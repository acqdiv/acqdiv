# -*- coding: UTF-8 -*-
""" Parser for Toolbox files for the Russian, Chintang and Indonesian corpora
"""

import re
import mmap
import logging
import contextlib
from itertools import zip_longest


class ToolboxFile(object):
    """ Toolbox Standard Format text file as iterable over records
    """
    _separator = re.compile(b'\r?\n\r?\n(\r?\n)')
    logging.basicConfig(filename='errors.log', level=logging.INFO)

    def __init__(self, config, file_path):
        """ Initializes a Toolbox file object

        Args:
            config: the corpus config file
            file_path: the file path to the session file
        """
        self.config = config
        self.path = file_path
        self.tier_separator = re.compile(b'\n')
        self.chintang_word_boundary = re.compile('(?<![\-\s])\s+(?![\-\s])')

        self.field_markers = []
        for k, v in self.config['record_tiers'].items():
            self.field_markers.append(k)

    def __iter__(self):
        """ Iterator that yields utterance, words, morphemes and inference information from a session transcript file.
        
        Note:
            This iterator directly extracts utterances for the db column utterance_raw and calls various
            functions to extract information from the following levels:

            get_sentence_type: extract the sentence type
            clean_utterance: clean-up the utterance
            get_warnings: get warnings like "transcription insecure"
            get_words: extract the words in an utterance for the words table
            get_morphemes extract the morphemes in a word for the morphemes table

        Returns:
            utterance: {}
            words: [{},{}...]
            morphemes: [[{},{}...], [{},{}...]...]
        """
        # FYI: the record marker needs to be updated if the corpus doesn't use "\ref" for record markers
        record_marker = re.compile(br'\\ref')
        with open(self.path, 'rb') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as data:
                ma = record_marker.search(data)
                header = data[:ma.start()].decode()
                pos = ma.start()

                for ma in record_marker.finditer(data, ma.end()):
                    utterance = {}
                    record = data[pos:ma.start()]
                    tiers = self.tier_separator.split(record)

                    for tier in tiers:
                        tokens = re.split(b'\\s+', tier, maxsplit=1)
                        field_marker = tokens[0].decode()
                        field_marker = field_marker.replace("\\", "")
                        content = None

                        if len(tokens) > 1:
                            content = tokens[1].decode()
                            content = re.sub('\\s+', ' ', content)

                        if field_marker in self.field_markers:
                            utterance[self.config['record_tiers'][field_marker]] = content

                    try:
                        utterance['utterance_raw'] = utterance[self.config['utterance']['field']]
                    except KeyError:
                        utterance['warning'] = 'empty utterance'

                    # Skip the first rows that contain metadata information:
                    # https://github.com/uzling/acqdiv/issues/154
                    if 'utterance_raw' in utterance.keys() and not utterance['utterance_raw'] is None:
                        # https://github.com/uzling/acqdiv/issues/379
                        if not utterance['utterance_raw'].startswith('@'):
                            if self.config['corpus']['corpus'] == 'Chintang':
                                try:
                                    utterance['sentence_type'] = self.get_sentence_type(utterance['nepali'])
                                    del utterance['nepali']
                                    if utterance['translation'] == None:
                                        del utterance['translation']
                                except KeyError:
                                    continue

                            elif self.config['corpus']['corpus'] == 'Russian':
                                try:
                                    utterance['sentence_type'] = self.get_sentence_type(utterance['utterance_raw'])
                                    utterance['utterance_raw'] = re.sub('xxx?|www', '???', utterance['utterance_raw'])
                                    utterance['pos_raw'] = re.sub('xxx?|www', '???', utterance['pos_raw'])
                                except KeyError:
                                    continue
                            else:
                                utterance['sentence_type'] = self.get_sentence_type(utterance['utterance_raw'])

                            utterance['utterance'] = self.clean_utterance(utterance['utterance_raw'])
                            utterance['warning'] = self.get_warnings(utterance['utterance_raw'])

                            words = self.get_words(utterance['utterance'])
                            morphemes = self.get_morphemes(utterance)

                            yield utterance, words, morphemes
                            pos = ma.start()
                """
                # in case of footer
                ma = self._separator.search(data, pos)
                if ma is None:
                    footer = ''
                    yield data[pos:].decode()
                else:
                    footer = data[ma.start(1):].decode()
                    yield data[pos:ma.start(1)].decode()
                self.header, self.footer = header, footer
                """

    def get_words(self, utterance):
        """ Return ordered list of words where each word is a dict of key-value pairs
        
        This function does Toolbox corpus-specific word processing and distinguishes between
        word and word_target if necessary.
        
        Args:
            utterance: str
            
        Returns:
            result: A list of ordered dictionaries with word and parent utterance id (utterance_id_fk).
        """
        result = []
        words = utterance.split()

        for word in words:
            d = {}
            if self.config['corpus']['corpus'] == 'Indonesian':
                # Distinguish between word and word_target; otherwise the target word is identical to the actual word:
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1859-L1867
                # Also: xx(x), www and *** is garbage from chat
                if re.search('\(', word):
                    d['word_target'] = re.sub('[\(\)]', '', word)
                    d['word'] = re.sub('\([^\)]+\)', '', word)
                    result.append(d)
                else:
                    d['word_target'] = re.sub('xxx?|www', '???', word)
                    d['word'] = re.sub('xxx?', '???', word)
                    result.append(d)
            else:
                d['word'] = re.sub('xxx?|www|\*\*\*', '???', word)
                # Actual vs target distinction <forehead slap>
                # if self.config['corpus']['corpus'] in ['Chintang', 'Russian']:
                #    word['word_actual'] = word['word']
                result.append(d)

        # TODO: get words and morphemes

        return result

    def get_sentence_type(self, utterance):
        """ Get utterance type (aka sentence type) of an utterance: default, question, imperative or exclamation.

        Args:
            utterance: str
            
        Returns:
            sentence_type: str
        """
        if self.config['corpus']['corpus'] == "Russian":
            match_punctuation = re.search('([\.\?!])$', utterance)
            if match_punctuation is not None:
                sentence_type = None
                if match_punctuation.group(1) == '.':
                    sentence_type = 'default'
                if match_punctuation.group(1) == '?':
                    sentence_type = 'question'
                if match_punctuation.group(1) == '!':
                    sentence_type = 'imperative'
                return sentence_type

        if self.config['corpus']['corpus'] == "Indonesian":
            if re.search('\.', utterance):
                return 'default'
            elif re.search('\?\s*$', utterance):
                return 'question'
            elif re.search('\!', utterance):
                return 'imperative'
            else:
                return

        # https://github.com/uzling/acqdiv/issues/253
        # \eng: . = default, ? = question, ! = exclamation
        # \nep: । = default, rest identical. Note this is not a "pipe" but the so-called danda at U+0964
        if self.config['corpus']['corpus'] == "Chintang":
            if not utterance is None:
                match_punctuation = re.search('([।\?!])$', utterance)
                if match_punctuation is not None:
                    sentence_type = None
                    if match_punctuation.group(1) == '।':
                        sentence_type = 'default'
                    if match_punctuation.group(1) == '?':
                        sentence_type = 'question'
                    if match_punctuation.group(1) == '!':
                        sentence_type = 'exclamation'
                    return sentence_type

    def get_warnings(self, utterance):
        """ Extracts warnings for insecure transcriptions for Russian and Indonesian (incl. intended form for Russian).

        Args:
            utterance: str
        
        Returns:
            transcription_warning: str
        """
        if self.config['corpus']['corpus'] == "Russian":
            if re.search('\[(\s*=?.*?|\s*xxx\s*)\]', utterance):
                for target in re.findall('\[=\?\s+[^\]]+\]', utterance):
                    target_clean = re.sub('["\[\]\?=]','',target)
                    transcription_warning = 'transcription insecure (intended form might have been "' + target_clean +'")'
                    return transcription_warning
                
        if self.config['corpus']['corpus'] == "Indonesian":
                # Insecure transcription [?], add warning, delete marker
                # cf. https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1605-1610
                if re.search('\[\?\]', utterance):
                    utterance = re.sub('\[\?\]', '', utterance)
                    transcription_warning = 'transcription insecure'
                    return transcription_warning
        else:
            pass

    def clean_utterance(self, utterance):
        """ Cleans up corpus-specific utterances from punctuation marks, comments, etc.

        Args:
            utterance: str
            
        Returns:
            utterance: str
        """
        
        # TODO: incorporate Russian \pho and \text tiers -- right now just utterance in general
        # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1586-L1599
        if not utterance is None: # != 'None' or utterance != '':
            if self.config['corpus']['corpus'] == "Russian":
                utterance = re.sub('[‘’\'“”\"\.!,:\+\/]+|(&lt; )|(?<=\\s)\?(?=\\s|$)', '', utterance)
                utterance = re.sub('\\s\-\\s', ' ', utterance)

                ## TODO: Not sure how to get warnings that are on utterance (and not word/morpheme) level
                # Insecure transcriptions [?], [=( )?], [xxx]: add warning, delete marker
                # Note that [xxx] usually replaces a complete utterance and is non-aligned,
                # in contrast to xxx without brackets, which can be counted as a word
                if re.search('\[(\s*=?.*?|\s*xxx\s*)\]', utterance):
                    utterance = re.sub('\[\s*=?.*?\]', '', utterance)

                utterance = re.sub('\s+', ' ', utterance).replace('=', '')
                utterance = utterance.strip()

                return utterance

            # incorporate the Indonesian stuff
            if self.config['corpus']['corpus'] == "Indonesian":
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1633-L1648
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1657-L1661
                # delete punctuation and garbage
                utterance = re.sub('[‘’\'“”\"\.!,;:\+\/]|\?$|<|>', '', utterance)
                utterance = re.sub('xxx?|www', '???', utterance)
                utterance = utterance.strip()
                                    
                # Insecure transcription [?], add warning, delete marker
                # cf. https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1605-1610
                if re.search('\[\?\]', utterance):
                    utterance = re.sub('\[\?\]', '', utterance)

                return utterance
    
            if self.config['corpus']['corpus'] == "Chintang":
                # No specific stuff here.
                return utterance

    def get_morphemes(self, utterance):
        """ Return ordered list of lists of morphemes where each morpheme is a dict of key-value pairs

        Args:
            utterance: a dict of utterance information

        Returns:
            result: a list of lists that contain dicts
        """
        result = []
        morphemes = []
        poses = [] # parts of speeches :)
        glosses = []
        warnings = []

        # Russian specific morpheme inference
        if self.config['corpus']['corpus'] == "Russian":
            if 'morpheme' in utterance.keys():
                # Remove punctuation from morphemes
                morphemes_cleaned = re.sub('[‘’\'“”\"\.!,:\-\?\+\/]', '', utterance['morpheme'])
                morphemes_cleaned = re.sub('xxx?|www', '???', morphemes_cleaned)
                morphemes = morphemes_cleaned.split()

            if 'pos_raw' in utterance.keys():
                # Get pos and gloss, see:
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1751-L1762)

                # Remove PUNCT pos
                pos_cleaned = utterance['pos_raw'].replace('PUNCT', '').replace('ANNOT','').replace('<NA: lt;> ','').split()

                # The Russian tier \mor contains both glosses and POS, separated by "-" or ":".
                # Method for distinguishing and extracting them:
                for pos in pos_cleaned:
                    # 1) If there is no ":" in a word string, gloss and POS are identical (most frequently the case with
                    # PCL 'particle').
                    if ':' not in pos:
                        poses.append(re.sub('xxx?', '???', pos))
                        glosses.append(re.sub('xxx?', '???', pos))

                    # 2) Sub-POS are always separated by "-" (e.g. PRO-DEM-NOUN), subglosses are always separated by ":"
                    # (e.g. PST:SG:F). What varies, though, is the character that separates POS from glosses in the word
                    # string: If the POS is V ('verb') or ADJ ('adjective'), the glosses start behind the first "-",
                    # e.g. V-PST:SG:F:IRREFL:IPFV -> POS V, gloss PST.SG.F.IRREFL.IPFV
                    elif pos.startswith('V') or pos.startswith('ADJ'):
                        match_verb_adj = re.search('(V|ADJ)-(.*$)', pos)
                        if match_verb_adj:
                            poses.append(re.sub('xxx?', '???', match_verb_adj.group(1)))
                            glosses.append(re.sub('xxx?', '???', match_verb_adj.group(2)))

                    # 3) For all other POS, the glosses start behind the first ":", e.g. PRO-DEM-NOUN:NOM:SG ->
                    # POS PRO.DEM.NOUN, gloss NOM.SG
                    else:
                        match_gloss_pos = re.search('(^[^(V|ADJ)].*?):(.*$)', pos)
                        if match_gloss_pos:
                            poses.append(re.sub('xxx?', '???', match_gloss_pos.group(1)))
                            glosses.append(re.sub('xxx?', '???', match_gloss_pos.group(2)))
            else:
                warnings.append('not glossed')

        # Indonesian specific morpheme inference stuff
        elif self.config['corpus']['corpus'] == "Indonesian":
            if 'morpheme' in utterance.keys():
                # remove punctuation from morphemes
                morphemes_cleaned = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterance['morpheme'])
                morphemes_cleaned = re.sub('xxx?|www', '???', morphemes_cleaned)
                morphemes = morphemes_cleaned.split()

            if 'gloss_raw' in utterance.keys():
                glosses_Indonesian = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterance['gloss_raw'])
                glosses_Indonesian = re.sub('xxx?|www', '???', glosses_Indonesian)
                glosses = glosses_Indonesian.split()
            else:
                warnings.append('not glossed')

        # Chintang specific morpheme stuff
        elif self.config['corpus']['corpus'] == "Chintang":
            if 'morpheme' in utterance.keys():
                # Remove non-linguistic punctuation from morphemes
                morphemes_cleaned = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterance['morpheme'])

                # Replace pos automatically tagged "***" (fail) with "???" (unknown)
                morphemes_cleaned = re.sub('\*\*\*', '???', morphemes_cleaned)

                # Chintang morphemes AND words are space delimited, e.g. 'hap -i -nig hap -i -nig'
                # we need to infer first the word boundaries and then the morphemes
                # words = re.sub('(\s\-)|(\-\s)','-', morphemes_cleaned)

                # word_boundaries = re.sub('(\s\-)|(\-\s)','%%%%%', morphemes_cleaned)
                word_boundaries = re.split(self.chintang_word_boundary, morphemes_cleaned)
                for word in word_boundaries:
                    morphemes.append(word.split())
                # print("morphemes:", morphemes)
            else:
                warnings.append('no morpheme tier')

            if 'gloss_raw' in utterance.keys():
                word_boundaries = re.split(self.chintang_word_boundary, utterance['gloss_raw'])
                for word in word_boundaries:
                    glosses.append(word.split())
                # print("glosses:", glosses)
            else:
                warnings.append('not glossed')

            if 'pos_raw' in utterance.keys():
                word_boundaries = re.split(self.chintang_word_boundary, utterance['pos_raw'])
                for word in word_boundaries:
                    poses.append(word.split())
                # print("poses:", poses)
            else:
                warnings.append('pos missing')

            # TODO: log this stuff
            if len(morphemes) == len(glosses) == len(poses):
                # Loop over the "words" to create nested lists of morphemes
                # Note this will return mismatched words-to-morphemes if the input tiers are wrong (but those errors are logged)
                for i in range(0, len(morphemes)):
                    l = []
                    # for (morph, gloss, pos, warning) in zip_longest(morphemes[i], glosses[i], poses[i], warnings[i]):
                    for (morph, gloss, pos) in zip_longest(morphemes[i], glosses[i], poses[i]):
                        d = {}
                        d['morpheme'] = morph
                        d['gloss_raw'] = gloss
                        d['pos_raw'] = pos
                        # d['warning'] = warning
                        l.append(d)
                    result.append(l)
                # print()
            else:
                logging.info("Length of morphemes, glosses, poses don't match:" + utterance['source_id'])
        return result

    def make_rec(self, data):
        # probably not needed
        return data.decode(self.encoding)

    def __repr__(self):
        # for pretty printing
        return '%s(%r)' % (self.__class__.__name__, self.path)

@contextlib.contextmanager
def memorymapped(path, access=mmap.ACCESS_READ):
    """ Return a block context with path as memory-mapped file. """
    fd = open(path)
    try:
        m = mmap.mmap(fd.fileno(), 0, access=access)
    except:
        fd.close()
        raise
    try:
        yield m
    finally:
        m.close()
        fd.close()

if __name__ == "__main__":
    from parsers import CorpusConfigParser
    cfg = CorpusConfigParser()
    cfg.read("ini/Chintang.ini")
    f = "tests/corpora/Chintang/Toolbox/Chintang.txt"
    # cfg.read("Russian.ini")
    # f = "../../corpora/Russian/toolbox/A00210817.txt"
    t = ToolboxFile(cfg, f)
    for record in t:
        print(record)
        # for k, v in record.items():
        #    print(k, "\t", v)
