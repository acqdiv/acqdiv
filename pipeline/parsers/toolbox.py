# -*- coding: utf-8 -*-
""" Parser for Toolbox files for the Russian, Chintang and Indonesian corpora
"""

import sys
import re
import mmap
import logging
import contextlib
from itertools import zip_longest

# logging.basicConfig(filename='toolbox.log', level=logging.INFO)
logger = logging.getLogger('pipeline' + __name__)

class ToolboxFile(object):
    """ Toolbox Standard Format text file as iterable over records
    """
    _separator = re.compile(b'\r?\n\r?\n(\r?\n)')
    _record_marker = re.compile(br'\\ref')

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

        # get database column names
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
            FYI: the record marker needs to be updated if the corpus doesn't use "\ref" for record markers

        Returns:
            utterance: {}
            words: [{},{}...]
            morphemes: [[{},{}...], [{},{}...]...]
        """
        with open(self.path, 'rb') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as data:
                ma = self._record_marker.search(data)
                # Skip the first rows that contain metadata information: https://github.com/uzling/acqdiv/issues/154
                header = data[:ma.start()].decode()
                pos = ma.start()
                for ma in self._record_marker.finditer(data, ma.end()):
                    yield self.make_rec(data[pos:ma.start()])
                    pos = ma.start()
                if ma is None:
                    raise StopIteration
                else:
                    yield self.make_rec(data[pos:])


    def make_rec(self, record):
        """ Parse and make utterance, words and morpheme structures.
        :param data:
        :return:
        """
        utterance = {}
        words = []
        morphemes = []

        warnings = []
        tiers = self.tier_separator.split(record)
        for tier in tiers:
            tokens = re.split(b'\\s+', tier, maxsplit=1)
            field_marker = tokens[0].decode()
            field_marker = field_marker.replace("\\", "")
            content = None

            if len(tokens) > 1:
                content = tokens[1].decode()
                content = re.sub('\\s+', ' ', content)
                content = content.strip()
                if content.startswith('@') or content == "":
                    # TODO: log
                    continue

            if field_marker in self.field_markers:
                utterance[self.config['record_tiers'][field_marker]] = content
                if content is None:
                    warnings.append(self.config['record_tiers'][field_marker])

        # Some records will not have an utterance, append None for convenience below
        if not 'utterance_raw' in utterance:
            utterance['utterance_raw'] = None

        utterance['sentence_type'] = None if utterance['utterance_raw'] is None else self.get_sentence_type(utterance)

        # We infer sentence type from Chintang \nep but we do not add the nepali field to the database yet
        if self.config['corpus']['corpus'] == 'Chintang':
            if 'nepali' in utterance:
                del utterance['nepali']

        # Clean up Russian
        if self.config['corpus']['corpus'] == 'Russian':
            utterance['utterance_raw'] = None if utterance['utterance_raw'] is None else re.sub('xxx?|www', '???', utterance['utterance_raw'])
            utterance['pos_raw'] = None if utterance['pos_raw'] is None else re.sub('xxx?|www', '???', utterance['pos_raw'])
        # Create clean utterance
        utterance['utterance'] = None if utterance['utterance_raw'] is None else self.clean_utterance(utterance['utterance_raw'])

        # Talk to Robert
        # utterance['morpheme'] = None if not 'morpheme' in utterance else self.clean_morpheme(utterance['morpeheme'])
        # utterance['pos_raw'] = None if not 'morpheme' in utterance else self.clean_morpheme(utterance['pos_raw'])
        # utterance['gloss_raw'] = None if not 'morpheme' in utterance else self.clean_morpheme(utterance['gloss_raw'])

        # Append utterance warnings if data fields are missing in the input
        if not utterance['utterance_raw'] is None:
            if not self.get_warnings(utterance['utterance_raw']) is None:
                warnings.append(self.get_warnings(utterance['utterance_raw']))
        if len(warnings) > 0:
            utterance['warning'] = "Empty value in the input for: "+", ".join(warnings)

        # Create words and morphemes
        words = [] if utterance['utterance'] is None else self.get_words(utterance['utterance'])
        morphemes = [] if utterance['utterance'] is None else self.get_morphemes(utterance)

        return utterance, words, morphemes


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
                    d['word_actual'] = d['word']
                    result.append(d)
                else:
                    d['word_target'] = re.sub('xxx?|www', '???', word)
                    d['word'] = re.sub('xxx?', '???', word)
                    d['word_actual'] = d['word']
                    result.append(d)
            else:
                d['word'] = re.sub('xxx?|www|\*\*\*', '???', word)
                # Actual vs target distinction <forehead slap>
                if self.config['corpus']['corpus'] in ['Chintang', 'Russian']:
                    d['word_actual'] = word
                result.append(d)
        return result


    def get_sentence_type(self, utterance):
        """ Get utterance type (aka sentence type) of an utterance: default, question, imperative or exclamation.

        Args:
            utterance: str
            
        Returns:
            sentence_type: str
        """
        if self.config['corpus']['corpus'] == "Russian":
            match_punctuation = re.search('([\.\?!])$', utterance['utterance_raw'])
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
            if re.search('\.', utterance['utterance_raw']):
                return 'default'
            elif re.search('\?\s*$', utterance['utterance_raw']):
                return 'question'
            elif re.search('\!', utterance['utterance_raw']):
                return 'imperative'
            else:
                return None

        # https://github.com/uzling/acqdiv/issues/253
        # \eng: . = default, ? = question, ! = exclamation
        # \nep: । = default, rest identical. Note this is not a "pipe" but the so-called danda at U+0964
        if self.config['corpus']['corpus'] == "Chintang":
            if 'nepali' in utterance.keys() and not utterance['nepali'] is None:
                match_punctuation = re.search('([।\?!])$', utterance['nepali'])
                if match_punctuation is not None:
                    sentence_type = None
                    if match_punctuation.group(1) == '।':
                        sentence_type = 'default'
                    if match_punctuation.group(1) == '?':
                        sentence_type = 'question'
                    if match_punctuation.group(1) == '!':
                        sentence_type = 'exclamation'
                    return sentence_type
            elif 'eng' in utterance.keys() and not utterance['translation'] is None:
                match_punctuation = re.search('([।\?!])$', utterance['translation'])
                if match_punctuation is not None:
                    sentence_type = None
                    if match_punctuation.group(1) == '.':
                        sentence_type = 'default'
                    if match_punctuation.group(1) == '?':
                        sentence_type = 'question'
                    if match_punctuation.group(1) == '!':
                        sentence_type = 'exclamation'
                    return sentence_type
            else:
                return None


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
                utterance = re.sub('\*\*\*', '???', utterance)
                return utterance

    """ TODO: talk to Robert
    # Clean up Chintang
    if self.config['corpus']['corpus'] == 'Chintang':
        utterance['morpheme'] = None if utterance['morpheme'] is None else re.sub('\*\*\*', '???', utterance['morpheme'])
        utterance['gloss_raw'] = None if utterance['gloss_raw'] is None else re.sub('\*\*\*', '???', utterance['gloss_raw'])
        utterance['pos_raw'] = None if utterance['pos_raw'] is None else re.sub('\*\*\*', '???', utterance['pos_raw'])
        # We infer sentence type from Chintang \nep but we do not add the nepali field to the database yet
        if 'nepali' in utterance:
            del utterance['nepali']

    # Clean up Russian
    if self.config['corpus']['corpus'] == 'Russian':
        utterance['utterance_raw'] = None if utterance['utterance_raw'] is None else re.sub('xxx?|www', '???', utterance['utterance_raw'])
        utterance['pos_raw'] = None if utterance['pos_raw'] is None else re.sub('xxx?|www', '???', utterance['pos_raw'])
        utterance['morpheme'] = None if utterance['morpheme'] is None else re.sub('xxx?|www', '???', utterance['morpheme'])

    # Clean up Indonesian
    if self.config['corpus']['corpus'] == 'Russian':
        utterance['morpheme'] = None if utterance['morpheme'] is None else re.sub('xxx?|www', '???', utterance['morpheme'])
        utterance['gloss_raw'] = None if utterance['gloss_raw'] is None else re.sub('xxx?|www', '???', utterance['gloss_raw'])
        utterance['utterance_raw'] = None if utterance['utterance_raw'] is None else re.sub('xxx?|www', '???', utterance['utterance_raw'])
        utterance['translation'] = None if utterance['translation'] is None else re.sub('xxx?|www', '???', utterance['translation'])

    # Create clean utterance
    utterance['utterance'] = None if utterance['utterance_raw'] is None else self.clean_utterance(utterance['utterance_raw'])
    """

    def get_morphemes(self, utterance):
        """ Return ordered list of lists of morphemes where each morpheme is a dict of key-value pairs

        Args:
            utterance: a dict of utterance information

        Returns:
            result: a list of lists that contain dicts of morphemes and their gloss and pos
        """
        result = []
        morphemes = []
        poses = [] # parts of speeches :)
        glosses = []
        warnings = []

        # Russian specific morpheme inference
        if self.config['corpus']['corpus'] == "Russian":
            if 'pos_raw' in utterance.keys():
                # remove PUNCT pos
                pos_cleaned = [] if utterance['pos_raw'] is None else utterance['pos_raw'].replace('PUNCT', '').replace('ANNOT','').replace('<NA: lt;> ','').split()

            if 'morpheme' in utterance.keys():
                # Remove punctuation from morphemes
                morphemes_cleaned = re.sub('[‘’\'“”\"\.!,:\-\?\+\/]', '', utterance['morpheme'])
                morphemes_cleaned = re.sub('xxx?|www', '???', morphemes_cleaned)
                morphemes_split = morphemes_cleaned.split()
                morphemes = [morphemes_split[i:i+1] for i in range(0, len(morphemes_split), 1)] # make list of lists

            if 'pos_raw' in utterance.keys():
                # Get pos and gloss in Russian, see:
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1751-L1762)

                # Remove PUNCT in POS; if the POS in input data is missing, insert empty list for processing
                # TODO: log it
                pos_cleaned = [] if utterance['pos_raw'] is None else utterance['pos_raw'].replace('PUNCT', '').replace('ANNOT','').replace('<NA: lt;> ','').split()


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

                # Make list of lists to follow the structure of the other languages
                poses = [poses[i:i+1] for i in range(0, len(poses), 1)]
                glosses = [glosses[i:i+1] for i in range(0, len(glosses), 1)]

            else:
                warnings.append('not glossed')

        # Indonesian specific morpheme inference stuff
        elif self.config['corpus']['corpus'] == "Indonesian":
            if 'morpheme' in utterance.keys():
                # TODO: move this to post-processing?
                # Remove punctuation from morphemes
                morphemes_cleaned = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterance['morpheme'])
                morphemes_cleaned = re.sub('xxx?|www', '???', morphemes_cleaned)
                morphemes_split = morphemes_cleaned.split()
                morphemes = [morphemes_split[i:i+1] for i in range(0, len(morphemes_split), 1)]

            if 'gloss_raw' in utterance.keys():
                # TODO: move this to post-processing?
                glosses_Indonesian = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterance['gloss_raw'])
                glosses_Indonesian = re.sub('xxx?|www', '???', glosses_Indonesian)
                glosses_split = glosses_Indonesian.split()
                glosses = [glosses_split[i:i+1] for i in range(0, len(glosses_split), 1)]
                # There are no POS in Indonesian, so we populate empty data that becomes NULL in the database.
                poses = [[] for i in range(0, len(glosses_split), 1)]
            else:
                warnings.append('not glossed')
                # TODO: add in some logic to extract relevant source 'nt' (comment) field?

        # Chintang specific morpheme stuff
        elif self.config['corpus']['corpus'] == "Chintang":
            if 'morpheme' in utterance.keys():
                # Remove non-linguistic punctuation from morphemes
                morphemes_cleaned = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterance['morpheme'])

                # TODO: this should go to post-processing
                # Replace pos automatically tagged "***" (fail) with "???" (unknown)
                morphemes_cleaned = re.sub('\*\*\*', '???', morphemes_cleaned)

                # Chintang morphemes AND words are space delimited, e.g. 'hap -i -nig hap -i -nig'
                # we need to infer first the word boundaries and then the morphemes
                # words = re.sub('(\s\-)|(\-\s)','-', morphemes_cleaned)

                # word_boundaries = re.sub('(\s\-)|(\-\s)','%%%%%', morphemes_cleaned)
                word_boundaries = re.split(self.chintang_word_boundary, morphemes_cleaned)
                for word in word_boundaries:
                    # TODO: double check this logic is correct with Robert
                    word = word.replace(" - ", " ") # remove floating clitic marker
                    morphemes.append(word.split())
            else:
                warnings.append('no morpheme tier')

            if 'gloss_raw' in utterance.keys():
                word_boundaries = re.split(self.chintang_word_boundary, utterance['gloss_raw'])
                for word in word_boundaries:
                    word = word.replace(" - ", " ") # remove floating clitic marker
                    glosses.append(word.split())
            else:
                warnings.append('not glossed')

            if 'pos_raw' in utterance.keys():
                word_boundaries = re.split(self.chintang_word_boundary, utterance['pos_raw'])
                for word in word_boundaries:
                    word = word.replace(" - ", " ") # remove floating clitic marker
                    poses.append(word.split())
            else:
                warnings.append('pos missing')

        else:
            raise TypeError("Corpus format is not supported by this parser.")


        # This bit adds None (NULL in the DB) for any mis-alignments
        tiers = list(zip_longest(morphemes, glosses, poses, fillvalue=[]))
        for tier in tiers:
            alignment = zip_longest(tier[0], tier[1], tier[2], fillvalue=None)
            l = []
            for morpheme in alignment:
                d = {}
                d['morpheme'] = morpheme[0]
                d['gloss_raw'] = morpheme[1]
                d['pos_raw'] = morpheme[2]
                # TODO: move to postprocessing if faster
                d['type'] = self.config['morphemes']['type'] # what type of morpheme as defined in the corpus .ini
                d['warning'] = None if len(warnings) == 0 else " ".join(warnings)
                l.append(d)
                logger.info("Length of morphemes, glosses, poses don't match in the Toolbox file: " + utterance['source_id'])
            result.append(l)
        return result


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
