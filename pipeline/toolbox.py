""" Parse toolbox files
"""

import re
import mmap
import collections
import contextlib
from itertools import zip_longest

class ToolboxFile(object):
    """ Toolbox Standard Format text file as iterable over records """

    _separator = re.compile(b'\r?\n\r?\n(\r?\n)')

    def __init__(self, config, file_path):
        """ Initializes a Toolbox file object

        Args:
            config: the corpus config file
            file_path: the file path to the session file
        """
        self.path = file_path
        self.config = config
        self.tier_separator = re.compile(b'\n')
        self.field_markers = []

        for k, v in self.config['record_tiers'].items():
            self.field_markers.append(k)

        
    def __iter__(self):
        """ Iterator, yields raw utterances, words, morphemes and inference information from a Session file.
        
        Notes:
            This iterator directly extracts utterances for the db column utterance_raw and calls various
            functions to extract information from the following levels:

            sentence_type: Calls the function get_sentence_type() to extract the sentence type.
            clean_utterance: Calls the function clean_utterance() to the clean utterance.
            warnings: Calls the function get_warnings() to ge the warnings like "transcription insecure".
            words: Calls the function get_words() to extract the single words.
            morphemes: Calls the function get_morphemes() to extract the single morphemes.
            inference: Calls the function do_inference() to infere the morpheme, pos and gloss information.

        Returns:
            utterances, words, morphemes, inferences and ordered dictionaries
        """
        record_marker = re.compile(br'\\ref') # has to be updated if some corpus doesn't use "\ref" for record markers
        with open (self.path, 'rb') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as data:
                ma = record_marker.search(data)
                header = data[:ma.start()].decode()
                pos = ma.start()

                for ma in record_marker.finditer(data, ma.end()):
                    utterances = collections.OrderedDict()
                    record = data[pos:ma.start()]
                    tiers = self.tier_separator.split(record)

                    for tier in tiers:
                        tokens = re.split(b'\\s+', tier, maxsplit=1)
                        field_marker = tokens[0].decode()
                        field_marker = field_marker.replace("\\", "")
                        content = "None"

                        if len(tokens) > 1:
                            content = tokens[1].decode()
                            content = re.sub('\\s+', ' ', content)

                        if field_marker in self.field_markers:
                            utterances[self.config['record_tiers'][field_marker]] = content

                    # we need to choose either the phonetic or orthographic transcription
                    # for the general 'utterance' field (from config); also add its type
                    
                    try:
                        utterances['utterance_raw'] = utterances[self.config['utterance']['field']]
                    except KeyError:
                        utterances['utterance_raw'] = ""
                        utterances['warning'] = 'empty utterance'

                    # Skip the first rows that contain metadata information
                    # cf. https://github.com/uzling/acqdiv/issues/154
                    if not utterances['utterance_raw'].startswith('@'):
                        if self.config['corpus']['corpus'] == 'Chintang':
                            try:
                                utterances['sentence_type'] = self.get_sentence_type(utterances['nepali'])
                                del utterances['nepali']
                            except KeyError:
                                continue
                        else:
                            utterances['sentence_type'] = self.get_sentence_type(utterances['utterance_raw'])
                        utterances['utterance'] = self.clean_utterance(utterances['utterance_raw'])
                        utterances['warning'] = self.get_warnings(utterances['utterance_raw'])
                            
                        words = self.get_words(utterances)
                        morphemes = self.get_morphemes(utterances)
                        inferences = self.do_inference(utterances)

                        yield utterances, words, morphemes, inferences
                        pos = ma.start()

                """
                ma = self._separator.search(data, pos)
                if ma is None:
                    footer = ''
                    yield data[pos:].decode()
                else:
                    footer = data[ma.start(1):].decode()
                    yield data[pos:ma.start(1)].decode()
                self.header, self.footer = header, footer
                """

    def get_words(self,utterances):
        """ Function that does Toolbox corpus-specific word processing.
        
        This function does Toolbox corpus-specific word processing and distinguishes between
        word and word_target if necessary.
        
        Args:
            utterances: An ordered dictionary of utterances.
            
        Returns:
            result: A list of ordered dictionaries with word and parent utterance id (utterance_id_fk).
        """
        result = []
        words = utterances['utterance'].split()
                    
        for word in words:
            d = collections.OrderedDict()
            if self.config['corpus']['corpus'] == 'Indonesian':
                d['utterance_id_fk'] = utterances['utterance_id']

                # distinguish between word and word_target:
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1859-L1867
                # otherwise the target word is identical to the actual word
                if re.search('\(', word):
                    d['word_target'] = re.sub('[\(\)]', '',word)
                    d['word'] = re.sub('\([^\)]+\)', '', word)
                    result.append(d)
                else:
                    d['word_target'] = word
                    d['word'] = word
                    result.append(d)
            else:
                d = collections.OrderedDict()
                d['word'] = word
                d['utterance_id_fk'] = utterances['utterance_id']
                result.append(d)
        return result

    def get_sentence_type(self, utterance):
        """ Function to get utterance type (aka sentence type) from an utterance.
        
        Args:
            utterance: A single utterance
            
        Returns:
            sentence_type: Distinguishes between default, question, imperativ and exclamation.
        """
        if self.config['corpus']['corpus'] == "Russian":
            match_punctuation = re.search('([\.\?!])$', utterance)
            if match_punctuation is not None:
                sentence_type = ''
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

        # is there Chintang utterance/sentence type?
        # logic according to @rabart (cf. https://github.com/uzling/acqdiv/issues/253):
        # \eng: . = default, ? = question, ! = exclamation
        # \nep: । = default, rest identical. Note this is not a "pipe" but the so-called danda.
        if self.config['corpus']['corpus'] == "Chintang":
            match_punctuation = re.search('([।\?!])$', utterance)
            if match_punctuation is not None:
                sentence_type = ''
                if match_punctuation.group(1) == '।':
                    sentence_type = 'default'
                if match_punctuation.group(1) == '?':
                    sentence_type = 'question'
                if match_punctuation.group(1) == '!':
                    sentence_type = 'exclamation'
                return sentence_type

    def get_warnings(self,utterance):
        """ Extracts warning for insecure transcriptions for Russian and Indonesian (incl. intended form for Russian).

        Args:
            utterance: a single utterance
        
        Returns:
            transcription_warning: warning for insecure transcription
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
                    transcription_warning ='transcription insecure'
                    return transcription_warning
        else:
            pass

    def clean_utterance(self, utterance):
        """ Cleans up corpus-specific utterances from punctuation marks, comments, etc.
        
        TODO: move this to a cleaning module that's imported, e.g. from pyclean import * as pyclean?

        Args:
            utterance: A single utterance
            
        Returns:
            utterance: The cleaned utterance
        """
        
        # TODO: incorporate Russian \pho and \text tiers -- right now just utterance in general
        # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1586-L1599
        if utterance != 'None' or utterance != '':
            if self.config['corpus']['corpus'] == "Russian":
                utterance = re.sub('[‘’\'“”\"\.!,:\+\/]+|(&lt; )|(?<=\\s)\?(?=\\s|$)', '', utterance)
                utterance = re.sub('\\s\-\\s', ' ', utterance)
                
                ## TODO: Not sure how to get warnings that are on utterance (and not word/morpheme) level
                # Insecure transcriptions [?], [=( )?], [xxx]: add warning, delete marker
                # Note that [xxx] usually replaces a complete utterance and is non-aligned,
                # in contrast to xxx without brackets, which can be counted as a word
                if re.search('\[(\s*=?.*?|\s*xxx\s*)\]', utterance):
                    utterance = re.sub('\[\s*=?.*?\]', '', utterance)
                return utterance

            # incorporate the Indonesian stuff
            if self.config['corpus']['corpus'] == "Indonesian":
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1633-L1648
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1657-L1661
                # delete punctuation and garbage
                utterance = re.sub('[‘’\'“”\"\.!,;:\+\/]|\?$|<|>', '', utterance)
                utterance = utterance.strip()
                                    
                # Insecure transcription [?], add warning, delete marker
                # cf. https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1605-1610
                if re.search('\[\?\]', utterance):
                    utterance = re.sub('\[\?\]', '', utterance)
                return utterance
    
            if self.config['corpus']['corpus'] == "Chintang":
                # No specific stuff here.
                return utterance
            

    def do_inference(self, utterances):
        """ Function to do corpus-specific inference of morpheme, pos_raw and gloss_raw correspondence.
        
        This function takes utterances from a session and extracts POS tags (pos_raw) and glosses (gloss_raw9 from them.
        From corpus-specific inference rules, the matching between morpheme, pos_raw and gloss_raw gets infered.
        It also extracts warnings on morpheme level (warning: "not glossed", "pos missing").
        
        Args:
            utterances: An ordered dictionary of utterances.
            
        Returns:
            result: A list of ordered dictionaries with pos_raw, gloss_raw, warning and parent utterance id (utterance_id_fk). 
        """
        result = []
        if self.config['corpus']['corpus'] == "Russian":
            if 'pos_raw' in utterances.keys():
                # remove PUNCT pos
                pos_cleaned = utterances['pos_raw'].replace('PUNCT', '').replace('ANNOT','').replace('<NA: lt;> ','').split()
                
                # get pos and gloss, see:
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1751-L1762)

                # The Russian tier \mor contains both glosses and POS, separated by "-" or ":".
                # Method for distinguishing and extracting them:
                #   1) If there is no ":" in a word string, gloss and POS are identical (most frequently the case with
                #    PCL 'particle').
                #   2) Sub-POS are always separated by "-" (e.g. PRO-DEM-NOUN), subglosses are always separated by ":"
                #    (e.g. PST:SG:F). What varies, though, is the character that separates POS from glosses in the word
                #    string: If the POS is V ('verb') or ADJ ('adjective'), the glosses start behind the first "-",
                #    e.g. V-PST:SG:F:IRREFL:IPFV -> POS V, gloss PST.SG.F.IRREFL.IPFV
                #   3) For all other POS, the glosses start behind the first ":", e.g. PRO-DEM-NOUN:NOM:SG ->
                #    POS PRO.DEM.NOUN, gloss NOM.SG
    
                for pos in pos_cleaned:
                    d = collections.OrderedDict()
                    ## 1)
                    if ':' not in pos:
                        d['utterance_id_fk'] = utterances['utterance_id']
                        d['pos_raw'] = pos
                        d['gloss_raw'] = pos
                        result.append(d)
                    ## 2)
                    elif pos.startswith('V') or pos.startswith('ADJ'):
                        match_verb_adj = re.search('(V|ADJ)-(.*$)', pos)
                        if match_verb_adj:
                            d['utterance_id_fk'] = utterances['utterance_id']
                            d['pos_raw'] = match_verb_adj.group(1)
                            d['gloss_raw'] = match_verb_adj.group(2)
                            result.append(d)
                    ## 3)
                    else:
                        match_gloss_pos = re.search('(^[^(V|ADJ)].*?):(.*$)', pos)
                        if match_gloss_pos:
                            d['utterance_id_fk'] = utterances['utterance_id']
                            d['pos_raw'] = match_gloss_pos.group(1)
                            d['gloss_raw'] = match_gloss_pos.group(2)
                            result.append(d)
            else:
                d = collections.OrderedDict()
                d['utterance_id_fk'] = utterances['utterance_id']
                d['pos_raw'] = ''
                d['gloss_raw'] = ''
                d['warning'] = 'not glossed'
                result.append(d)

        # Indonesian specific morpheme/inference stuff
        elif self.config['corpus']['corpus'] == "Indonesian":
            if 'gloss_raw' in utterances.keys():
                glosses_Indonesian = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterances['gloss_raw'])
                glosses = glosses_Indonesian.split()
                for gloss in glosses:
                    d = collections.OrderedDict()
                    d['utterance_id_fk'] = utterances['utterance_id']
                    d['gloss_raw'] = gloss
                    result.append(d)
            else:
                d = collections.OrderedDict()
                d['utterance_id_fk'] = utterances['utterance_id']
                d['gloss_raw'] = ''
                d['warning'] = 'not glossed'
                result.append(d)

        # Chintang specific morpheme/inference stuff
        elif self.config['corpus']['corpus'] == "Chintang":
            d = collections.OrderedDict()
            if 'morpheme' and 'gloss_raw' and 'pos_raw' in utterances.keys():
                morphemes_target_Chintang = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterances['morpheme'])
                morphemes_Chintang = morphemes_Chintang = re.sub('(\s\-)|(\-\s)','-', morphemes_target_Chintang)
                try:
                    glosses_Chintang = utterances['gloss_raw']
                except KeyError:
                    glosses_Chintang = ''
                    d['utterance_id_fk'] = utterances['utterance_id']
                    d['warning'] = 'not glossed (gloss missing)'
                    result.append(d)
                try:    
                    pos_Chintang = utterances['pos_raw']
                except KeyError:
                    pos_Chintang = ''
                    d['utterance_id_fk'] = utterances['utterance_id']
                    d['warning'] = 'pos missing'
                    result.append(d)
                    
                morphemes = morphemes_Chintang.split()
                morphemes_targets = morphemes_target_Chintang.split()
                glosses_targets = glosses_Chintang.split()
                pos_targets = pos_Chintang.split()
                morphemes_target_counter = 0
                
                for (morpheme_target, gloss,pos) in zip_longest(morphemes_targets, glosses_targets,pos_targets):
                    morphemes_target_counter += 1
                    d = collections.OrderedDict()
                    d['utterance_id_fk'] = utterances['utterance_id']
                    d['morpheme'] = morpheme_target
                    d['gloss_raw'] = gloss
                    d['pos_raw'] = pos
                    result.append(d)
            else:
                d = collections.OrderedDict()
                d['morpheme'] = ''
                d['utterance_id_fk'] = utterances['utterance_id']
                d['gloss_raw'] = ''
                d['pos_raw'] = ''
                d['warning'] = 'not glossed'
                result.append(d)
        
        return result

    def get_morphemes(self, utterances):
        """ Function to do the Toolbox corpus-specific morpheme processing.
        
        Args:
            utterances: utterances: An ordered dictionary of utterances.
        
        Returns:
            result: A list of ordered dictionaries with morpheme and parent utterance id (utterance_id_fk).
        """
        
        result = []
        if 'morpheme' in utterances.keys():
            # Russian specific morpheme stuff
            if self.config['corpus']['corpus'] == "Russian":
                # remove punctuation from morphemes!
                morphemes_cleaned = re.sub('[‘’\'“”\"\.!,:\-\?\+\/]', '', utterances['morpheme'])
                morphemes = morphemes_cleaned.split()
                for morpheme in morphemes:
                    # Note that there is no "morpheme_target" for Russian
                    d = collections.OrderedDict()
                    d['morpheme'] = morpheme
                    d['utterance_id_fk'] = utterances['utterance_id']
                    result.append(d)
                    
            ## Indonesian specific morpheme stuff
            elif self.config['corpus']['corpus'] == "Indonesian":
                # remove punctuation
                morhphemes_Indonesian = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterances['morpheme'])
                morphemes = morhphemes_Indonesian.split()
                for morpheme in morphemes:
                    d = collections.OrderedDict()
                    d['morpheme'] = morpheme
                    d['utterance_id_fk'] = utterances['utterance_id']
                    result.append(d)
                
            ## Chintang specific morpheme stuff
            elif self.config['corpus']['corpus'] == "Chintang":
                # remove punctuation
                morphemes_Chintang = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterances['morpheme'])
                morphemes_Chintang = re.sub('(\s\-)|(\-\s)','-', morphemes_Chintang)
                morphemes = morphemes_Chintang.split()
                for morpheme in morphemes:
                    d = collections.OrderedDict()
                    d['morpheme'] = morpheme
                    d['utterance_id_fk'] = utterances['utterance_id']
                    result.append(d)    
        else:
            d = collections.OrderedDict()
            d['morpheme'] = ''
            d['utterance_id_fk'] = utterances['utterance_id']
            d['warning']  = 'morpheme missing' 
            result.append(d)
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
    cfg.read("Chintang.ini")
    f = "../../corpora/Chintang/toolbox/CLDLCh1R01S02.txt"
    # cfg.read("Russian.ini")
    # f = "../../corpora/Russian/toolbox/A00210817.txt"
    t = ToolboxFile(cfg, f)
    for record in t:
        print(record)
        # for k, v in record.items():
        #    print(k, "\t", v)
