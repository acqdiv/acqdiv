""" Parse toolbox files
"""

import re
import sys
import os
import collections
import contextlib
import mmap
import re
from itertools import zip_longest

class ToolboxFile(object):
    """ Toolbox Standard Format text file as iterable over records """

    _separator = re.compile(b'\r?\n\r?\n(\r?\n)')

    def __init__(self, config, file_path):
        self.path = file_path
        self.config = config
        self.session_id = self.config['record_tiers']['record_marker']
        self.record_marker = self.config['record_tiers']['record_marker']

        #self.tier_matches = collections.OrderedDict()
        #for k, v in self.config['record_tiers'].items():
        #    b = bytearray(v.encode())
        #    self.tier_matches[k] = re.compile(b.decode())

        # self.record_marker = self.config['record_tiers']['record_marker']
        # self.regex = re.compile(self.record_marker, re.MULTILINE)
        # self._separator = re.compile(b'\r?\n\r?\n(\r?\n)')

        # self.record_separator = re.compile(b'\\n{2,}')
        self.tier_separator = re.compile(b'\n')
        self.field_markers = []

        for k, v in self.config['record_tiers'].items():
            self.field_markers.append(k)

        # TODO: get sentence type, etc...

        # TODO (lingdp): get that warnings stuff going!
        # colletc all warnings in an ordered dict with the following structure:
        # {utterance_id:[warning_a,warning_b,warning_c,...], utterance_id:[warning_a,warning_b,warning_c],...}
        self.warnings = collections.OrderedDict()
        #self.warnings['warning'] = []
        

    def __iter__(self):
        record_marker = re.compile(br'\\ref')
        with open (self.path, 'rb') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as data:
                ma = record_marker.search(data)
                header = data[:ma.start()].decode()
                pos = ma.start()
                for ma in record_marker.finditer(data, ma.end()):
                    utterances = collections.OrderedDict()
                    # utterances['session_id'] = self.session_id

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
                    
                    #TODO: the below two lines rais the error discussed in https://github.com/uzling/acqdiv/issues/154.
                    #utterances['utterance'] = utterances[self.config['utterance']['field']]
                    #utterances['utterance_type'] = self.config['utterance']['type']
                
                    try:
                        utterances['utterance'] = utterances[self.config['utterance']['field']]
                        utterances['utterance_type'] = self.config['utterance']['type']
                        self.warnings['parent_id'] = utterances['utterance_id']
                    except KeyError:
                        utterances['utterance'] = ""
                        utterances['utterance_type'] = ""
                        self.warnings['parent_id'] = utterances['utterance_id']
                        #self.warnings['warnings'] = []
                        self.warnings['warnings'] = 'empty utterance'
                        
                    # Skip the first rows that contain metadata information
                    # cf. https://github.com/uzling/acqdiv/issues/154
                    if not utterances['utterance'].startswith('@'):
                        
                        # TODO: build in the rules system per corpus...
                        # clean up utterance, add new data via Robert inferences, etc.
                        # here we can just pass around the session utterance dictionary
                        utterances['sentence_type'] = self.get_sentence_type(utterances['utterance'])
                        utterances['utterance_cleaned'] = self.clean_utterance(utterances['utterance'])
                        
                        # utterances['utterance_cleaned'] = self.clean_utterance(utterances['utterance'])
                        # print(utterances)
    
                        
                        words = self.get_words(utterances) # pass the dictionary
                        #print(words)
                        
                                        
                        ## add parent_id to warnings
                        #self.warnings['parent_id'] = utterances['utterance_id']
                        # print(self.warnings)
                        
                        ## morphemes
                        morphemes = self.get_morphemes(utterances)
                        
                        ## morpheme, gloss, pos inferences
                        inferences = self.do_inference(utterances)
    
                        # print(utterances)
                        # TODO: return three dictionaries...
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
        """ Do the Toolbox corpus-specific word processing
        :param utterance: ordered dictionary
        :return: list of ordered dictionaries with word and parent utterance id
        """
        result = []
        words = utterances['utterance_cleaned'].split()
        
        for word in words:
            d = collections.OrderedDict()
            if self.config['corpus']['corpus'] == 'Indonesian':
                d['utterance_id_fk'] = utterances['utterance_id']
                ## distinguish between word and word_target (après: https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1859-L1867)
                if re.search('\(', word):
                    d['word_target'] = re.sub('[\(\)]', '',word)
                    d['word'] = re.sub('\([^\)]+\)', '', word)
                    result.append(d)
                # otherwise the target word is identical to the actual word
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
        """ Get utterance type (aka sentence type)
        :param utterance:
        :return: sentence_type
        """
        if self.config['corpus']['corpus'] == "Russian":
            match_punctuation = re.search('([\.\?!])$', utterance)
            if match_punctuation is not None:
            #    return sentence_types[match_punctuation.group(1)]  ##@bambooforest, I get an error here: NameError: name 'sentence_types' is not defined
                sentence_type = ''
                if match_punctuation.group(1) == '.':
                    sentence_type = 'default'
                if match_punctuation.group(1) == '?':
                    sentence_type = 'question'
                if match_punctuation.group(1) == '!':
                    sentence_type = 'imperative'
                
                return sentence_type

        # does this logic make any sense? why not, if, if, if, fuck it return?
        if self.config['corpus']['corpus'] == "Indonesian":
            if re.search('\.', utterance):
                return 'default'
            elif re.search('\?\s*$', utterance):
                return 'question'
            elif re.search('\!', utterance):
                return 'imperative'
            else:
                return

        # TODO: is there Chintang utterance/sentence type?

    # TODO: move this to a cleaning module that's imported, e.g. from pyclean import * as pyclean
    def clean_utterance(self, utterance):
        """ Clean up corpus-specific utterances
        :param utterance:
        :return:
        """
        resutls_warnings = []
        # TODO: incorporate Russian \pho and \text tiers -- right now just utterance in general
        # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1586-L1599
        if utterance != 'None' or utterance != '':
            if self.config['corpus']['corpus'] == "Russian":
                # delete punctuation in \pho and \text tiers
                utterance = re.sub('[‘’\'“”\"\.!,:\+\/]+|(&lt; )|(?<=\\s)\?(?=\\s|$)', '', utterance)
                utterance = re.sub('\\s\-\\s', ' ', utterance)
                
                ## TODO: Not sure how to get warnings that are on utterance (and not word/morpheme) level
                # Insecure transcriptions [?], [=( )?], [xxx]: add warning, delete marker
                # Note that [xxx] usually replaces a complete utterance and is non-aligned,
                # in contrast to xxx without brackets, which can be counted as a word
                #if re.search('\[(\s*=?\s*\?\s*|\s*xxx\s*)\]', utterance): ## TODO: I think this doesn't match what it should? (a . missing? check line below)
                if re.search('\[(\s*=?.*?|\s*xxx\s*)\]', utterance):
                    #utterance = re.sub('\[\s*=?\s*\?\s*\]','',utterance)  ## TODO: again, I think this doesn't match what it should... (check line below)
                    utterance = re.sub('\[\s*=?.*?\]', '', utterance)
                    self.warnings['warning'] ='transcription insecure'
                return utterance

            # incorporate the Indonesian stuff
            if self.config['corpus']['corpus'] == "Indonesian":
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1633-L1648
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1657-L1661
                # delete punctuation and garbage
                utterance = re.sub('[‘’\'“”\"\.!,;:\+\/]|\?$|\.\.\.|<|>', '', utterance)
                
                # Insecure transcription [?], add warning, delete marker
                # cf. https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1605-1610
                if re.search('\[\?\]', utterance):
                    utterance = re.sub('\[\?\]', '', utterance)
                    self.warnings['warning'] ='transcription insecure'
                    
                
                #TODO: what about the first couple of lines in some Indonesian sessions that is actually metadata info? How to get rid of that?
                # cf.: https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1601-1603
                return utterance
    
            if self.config['corpus']['corpus'] == "Chintang":
                # No specific stuff here.
                return utterance
            
        # add warning for empty utterance
        else:
            self.warnings['warning'].append('empty utterance')

    def do_inference(self, utterances):
        result = []
        warnings_result = []
        
        #morphs = get_morphemes(utterances)
        if self.config['corpus']['corpus'] == "Russian":
            # TODO: do the Russian words / morphemes inference
            if 'pos' in utterances.keys():
            # remove PUNCT pos
            #if self.config['corpus']['corpus'] == "Russian":
                pos_cleaned = utterances['pos'].replace('PUNCT', '').replace('ANNOT','').replace('<NA: lt;> ','').split()
                
                # get pos and gloss (après: https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1751-L1762)
                #The Russian tier \mor contains both glosses and POS, separated by "-" or ":". Method for distinguishing and extracting them:
                #* 1) If there is no ":" in a word string, gloss and POS are identical (most frequently the case with PCL 'particle').
                #* 2) Sub-POS are always separated by "-" (e.g. PRO-DEM-NOUN), subglosses are always separated by ":" (e.g. PST:SG:F). What varies, though, is the character that separates POS from glosses in the word string:
                #* If the POS is V ('verb') or ADJ ('adjective'), the glosses start behind the first "-", e.g. V-PST:SG:F:IRREFL:IPFV -> POS V, gloss PST.SG.F.IRREFL.IPFV
                #* 3) For all other POS, the glosses start behind the first ":", e.g. PRO-DEM-NOUN:NOM:SG -> POS PRO.DEM.NOUN, gloss NOM.SG
    
                for pos in pos_cleaned:
                    d = collections.OrderedDict()
                    ## 1)
                    if ':' not in pos:
                        d['parent_id'] = utterances['utterance_id']
                        d['pos'] = pos
                        d['gloss'] = pos
                        result.append(d)
                    ## 2)
                    elif pos.startswith('V') or pos.startswith('ADJ'):
                        match_verb_adj = re.search('(V|ADJ)-(.*$)', pos)
                        if match_verb_adj:
                            d['parent_id'] = utterances['utterance_id']
                            d['pos'] = match_verb_adj.group(1)
                            d['gloss'] = match_verb_adj.group(2)
                            result.append(d)
                    ## 3)
                    else:
                        match_gloss_pos = re.search('(^[^(V|ADJ)].*?):(.*$)', pos)
                        if match_gloss_pos:
                            d['parent_id'] = utterances['utterance_id']
                            d['pos'] = match_gloss_pos.group(1)
                            d['gloss'] = match_gloss_pos.group(2)
                            result.append(d)
                            
            else:
                d = collections.OrderedDict()
                d['parent_id'] = utterances['utterance_id']
                d['pos'] = ''
                d['gloss'] = ''
                d['warning'] = 'not glossed!'
                result.append(d)
                        
        # Indonesian specific morpheme/inference stuff
        elif self.config['corpus']['corpus'] == "Indonesian":
            if 'gloss' in utterances.keys():
                glosses_Indonesian = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterances['gloss'])
                glosses = glosses_Indonesian.split()
                for gloss in glosses:
                    d = collections.OrderedDict()
                    d['parent_id'] = utterances['utterance_id']
                    d['gloss'] = gloss
                    result.append(d)
            else:
                d = collections.OrderedDict()
                d['parent_id'] = utterances['utterance_id']
                d['gloss'] = ''
                d['warning'] = 'not glossed!'
                result.append(d)
                
                
        # Chintang specific morpheme/inference stuff
        elif self.config['corpus']['corpus'] == "Chintang":
            d = collections.OrderedDict()
            if 'morpheme' and 'gloss' and 'pos' in utterances.keys():
                morphemes_target_Chintang = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterances['morpheme'])
                morphemes_Chintang = morphemes_Chintang = re.sub('(\s\-)|(\-\s)','-', morphemes_target_Chintang)
                #glosses_Chintang = utterances['gloss']
                #pos_Chintang = utterances['pos']
                try:
                    glosses_Chintang = utterances['gloss']
                except KeyError:
                    glosses_Chintang = ''
                    d['parent_id'] = utterances['utterance_id']
                    d['warning'] = 'not glossed!'
                    #self.warnings['warning'] = 'not glossed!'
                    result.append(d)
                try:    
                    pos_Chintang = utterances['pos']
                except KeyError:
                    pos_Chintang = ''
                    d['parent_id'] = utterances['utterance_id']
                    d['warning'] = 'pos missing!'
                    #self.warnings['warning'] = 'pos missing!'
                    result.append(d)
                    
                morphemes = morphemes_Chintang.split()
                morphemes_targets = morphemes_target_Chintang.split()
                glosses_targets = glosses_Chintang.split()
                pos_targets = pos_Chintang.split()
                morphemes_target_counter = 0
                
                for (morpheme_target, gloss,pos) in zip_longest(morphemes_targets, glosses_targets,pos_targets):
                    morphemes_target_counter += 1
                    d = collections.OrderedDict()
                    d['parent_id'] = utterances['utterance_id']
                    #d['morpheme_id'] = str(utterances['utterance_id'])+'_'+str(morphemes_target_counter) ## needed?
                    d['morpheme'] = morpheme_target
                    d['segment_target'] = morpheme_target
                    d['gloss_target'] = gloss
                    d['pos_target'] = pos
                    result.append(d)
            else:
                d = collections.OrderedDict()
                d['morpheme'] = ''
                d['segment_target'] = ''
                d['parent_id'] = utterances['utterance_id']
                #d['morpheme_id'] = '' ## needed??
                d['gloss_target'] = ''
                d['pos_target'] = ''
                d['warning'] = 'not glossed!'
                result.append(d)
                #self.warnings['warning'] ='not glossed!'
        
        return result

    def get_morphemes(self, utterances):
        """ Do the Toolbox corpus-specific morpheme processing
        :return: (so far) list of ordered dictionaries with morpheme and parent utterance id
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
                    d['segment_target'] = morpheme
                    d['parent_id'] = utterances['utterance_id']
                    result.append(d)
                    
            ## Indonesian specific morpheme stuff
            elif self.config['corpus']['corpus'] == "Indonesian":
                # remove punctuation
                morhphemes_Indonesian = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterances['morpheme'])
                morphemes = morhphemes_Indonesian.split()
                for morpheme in morphemes:
                    d = collections.OrderedDict()
                    d['morpheme'] = morpheme
                    d['segment'] = morpheme
                    d['parent_id'] = utterances['utterance_id']
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
                    d['parent_id'] = utterances['utterance_id']
                    result.append(d)    
        else:
            d = collections.OrderedDict()
            d['morpheme'] = ''
            d['parent_id'] = utterances['utterance_id']
            d['warning']  = 'morpheme missing!' 
            result.append(d)
            #self.warnings['warning'] = 'morpheme missing!'
                
        return result
    


    # probably not needed
    def make_rec(self, data):
        return data.decode(self.encoding)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.path)


class Record(collections.OrderedDict):
    """ Toolbox records in file """
    # report if record is missing
    pass


@contextlib.contextmanager
def memorymapped(path, access=mmap.ACCESS_READ):
    """Return a block context with path as memory-mapped file."""
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
        #for k, v in record.items():
        #    print(k, "\t", v)

    # should we clean the records here on a corpus-by-corpus basis?
    # or should we insert data structures as is into the db?


