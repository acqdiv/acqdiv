""" Parse toolbox files
"""

import re
import sys
import os
import collections
import contextlib
import mmap
import re

from parselib import t_correspondences as sentence_types

class ToolboxFile(object):
    """ Toolbox Standard Format text file as iterable over records """

    _separator = re.compile(b'\r?\n\r?\n(\r?\n)')

    def __init__(self, config, file_path):
        self.path = file_path
        self.config = config
        # what is this?
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

        # so we don't have to check the config on each iteration
        self.field_markers = []
        for k, v in self.config['record_tiers'].items():
            self.field_markers.append(k)

        # print("FIELD MARKERS")
        # print(self.field_markers)

        # collect the warnings
        # colletc all warnings in an ordered dict with the following structure:
        # {utterance_id:[warning_a,warning_b,warning_c,...], utterance_id:[warning_a,warning_b,warning_c],...}
        self.warnings = collections.OrderedDict()
        #self.warnings['warning'] = []
        

    # TODO: return utterances, words, morphemes, as ordered dictionaries?
    def __iter__(self):
        # TODO: move some of this stuff outside of the iterator, i.e. compile once the regexes
        record_marker = re.compile(br'\\ref')
        with open (self.path, 'rb') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as data:
                # TODO: skip the first metadata rows (they include \ref, but they include crap)
                # e.g. for Indonesian:
                # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1637-L1639

                ma = record_marker.search(data)
                header = data[:ma.start()].decode()
                pos = ma.start()
                for ma in record_marker.finditer(data, ma.end()):
                    utterances = collections.OrderedDict()
                    # utterances['session_id'] = self.session_id
                    # words = collections.OrderedDict()
                    # words['session_id'] = self.session_id

                    # process each record:
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
                            content = content.strip()
                            

                        # TODO: this needs to be moved to the end, i.e. return just what is specified in the config
                        if field_marker in self.field_markers:
                            utterances[self.config['record_tiers'][field_marker]] = content

                    # we need to choose either the phonetic or orthographic transcription
                    # for the general 'utterance' field (from config); also add its type
                    
                    #TODO: the below two lines rais the error discussed in https://github.com/uzling/acqdiv/issues/154, possible workaround: lines 92-98.
                    utterances['utterance'] = utterances[self.config['utterance']['field']]
                    utterances['utterance_type'] = self.config['utterance']['type']
                
                    #try:
                    #    utterances['utterance'] = utterances[self.config['utterance']['field']]
                    #    utterances['utterance_type'] = self.config['utterance']['type']
                    #except KeyError:
                    #    utterances['utterance'] = "None"
                    #    utterances['utterance_type'] = "None"
                    #    self.warnings['warnings'] = 'empty utterance' # <<-- add warning here?

                    # TODO: build in the rules system per corpus...
                    # clean up utterance, add new data via Robert inferences, etc.
                    # here we can just pass around the session utterance dictionary
                    utterances['sentence_type'] = self.get_sentence_type(utterances['utterance'])
                    utterances['utterance_cleaned'] = self.clean_utterance(utterances['utterance'])
                    
                    # utterances['utterance_cleaned'] = self.clean_utterance(utterances['utterance'])
                    # print(utterances)

                    # TODO: add in the words parsing (and inference?)
                    # how to handle this specifically?
                    # needs to live outside of utterance?
                    words = self.get_words(utterances) # pass the dictionary
                    #print('words')
                    #print(words)
                    
                                    
                    ## add parent_id to warnings
                    self.warnings['parent_id'] = utterances['utterance_id']
                    # print(self.warnings)
                    
                    

                    # TODO: add in the morpheme parsing and inference
                    morphemes = self.get_morphemes(utterances)
                    #print('morphemes')
                    #print(morphemes)
                    
                    inferences = self.do_inference(utterances)

                    # print(utterances)
                    # TODO: return three dictionaries...
                    # yield utterances, words, morphemes
                    yield utterances, words, morphemes, inferences, self.warnings
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
        # TODO: make sure to deal with the comment handling, etc., e.g.:
        # if self.config['corpus']['corpus'] == "Russian":
            # words_comments = re.search('(.*?)(\[=.*?\])', my_words)
        for word in words:
            d = collections.OrderedDict()
            d['word'] = word
            d['parent_id'] = utterances['utterance_id']
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
                return sentence_types[match_punctuation.group(1)]
            return

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
        # TODO: incorporate Russian \pho and \text tiers -- right now just utterance in general
        # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1586-L1599
        if utterance != 'None' or utterance != '':
            if self.config['corpus']['corpus'] == "Russian":
                # delete punctuation in \pho and \text tiers
                utterance = re.sub('[‘’\'“”\"\.!,:\+\/]+|(&lt; )|(?<=\\s)\?(?=\\s|$)', '', utterance)
                utterance = re.sub('\\s\-\\s', ' ', utterance)
                #utterance = utterance.replace('\s\s', ' ')
    
                # Insecure transcriptions [?], [=( )?], [xxx]: add warning, delete marker
                # Note that [xxx] usually replaces a complete utterance and is non-aligned,
                # in contrast to xxx without brackets, which can be counted as a word
                #if re.search('\[(\s*=?\s*\?\s*|\s*xxx\s*)\]', utterance): ## TODO: I think this doesn't match what it should? (a . missing? check line below)
                if re.search('\[(\s*=?.*?|\s*xxx\s*)\]', utterance):
                    #utterance = re.sub('\[\s*=?\s*\?\s*\]','',utterance)  ## TODO: again, I think this doesn't match what it should... (check line below)
                    utterance = re.sub('\[\s*=?.*?\]', '', utterance)
                    self.warnings['warning'] ='transcription insecure'
                return utterance

            # TODO: incorporate the Indonesian stuff
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
        #morphs = get_morphemes(utterances)
        if self.config['corpus']['corpus'] == "Russian":
            # TODO: do the Russian words / morphemes inference
            if 'pos' in utterances.keys():
            # remove PUNCT pos
            #if self.config['corpus']['corpus'] == "Russian":
                pos_cleaned = utterances['pos'].replace('PUNCT', '').replace('ANNOT','').replace('<NA: lt;> ','').split()
                
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
                d['pos'] = 'None'
                d['gloss'] = 'None'
                d['parent_id'] = utterances['utterance_id']
                result.append(d)
                self.warnings['warning'].append('not glossed!')
                        
        # TODO: Indonesian specific morpheme/inference stuff
        elif self.config['corpus']['corpus'] == "Indonesian":
            pass
        
        # TODO: Chintang specific morpheme/inference stuff
        elif self.config['corpus']['corpus'] == "Chintang":
            pass
        
        return result

    ## TODO, change, crap for now
    def get_morphemes(self, utterances):
        """ Do the Toolbox corpus-specific morpheme processing
        :return: (so far) list of ordered dictionaries with morpheme and parent utterance id
        """
        result = []
        
        if 'morpheme' in utterances.keys():
            # remove punctuation from morphemes!
            if self.config['corpus']['corpus'] == "Russian":
                morphemes_cleaned = re.sub('[‘’\'“”\"\.!,:\-\?\+\/]', '', utterances['morpheme'])
                morphemes = morphemes_cleaned.split()
                
                for morpheme in morphemes:
                    # Note that there is no "morpheme_target" for Russian
                    d = collections.OrderedDict()
                    d['morpheme'] = morpheme
                    d['parent_id'] = utterances['utterance_id']
                    result.append(d)
                    
            ## TODO: Indonesian specific morpheme stuff!!
            elif self.config['corpus']['corpus'] == "Indonesian":
                # remove punctuation
                morhphemes_Indonesian = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterances['morpheme'])
                morphemes = morhphemes_Indonesian.split()
                
                for morpheme in morphemes:
                    d = collections.OrderedDict()
                    d['morpheme'] = morpheme
                    d['parent_id'] = utterances['utterance_id']
                    result.append(d)
                
            #
            ## TODO: Chintang specific morpheme stuff!!
            elif self.config['corpus']['corpus'] == "Chintang":
                # remove punctuation
                morhphemes_Chintang = re.sub('[‘’\'“”\"\.!,:\?\+\/]', '', utterances['morpheme'])
                morphemes = morhphemes_Chintang.split()
                
                for morpheme in morphemes:
                    d = collections.OrderedDict()
                    d['morpheme'] = morpheme
                    d['parent_id'] = utterances['utterance_id']
                    result.append(d)
            
        else:
            d = collections.OrderedDict()
            #d['morpheme'] = 'None'
            d['parent_id'] = utterances['utterance_id']
            result.append(d)
            self.warnings['warning'] = 'morpheme missing!'
            
                
        return result



    # probably not needed
    def make_rec(self, data):
        return data.decode(self.encoding)

    # This is a nice way to print stuff for a class
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.path)


class Record(collections.OrderedDict):
    """ Toolbox records in file """
    # report if record is missing
    def __init__(**kwargs):
        pass

    def clean(self):
        # use Robert's cleaning functions
        pass

class UtteranceType(object):
    # form to function mapping from punctuation to sentence type
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

    # cfg.read("Chintang.ini")
    # f = "../../corpora/Chintang/toolbox/CLDLCh1R01S02.txt"

    cfg.read("Russian.ini")
    f = "../../corpora/Russian/toolbox/A00210817.txt"

    # cfg.read("Indonesian.ini")
    # f = "../../corpora/Indonesian/toolbox/HIZ-010601.txt"

    t = ToolboxFile(cfg, f)
    for record in t:
        pass
        # print(record)
        #for k, v in record.items():
        #    print(k, "\t", v)

    # should we clean the records here on a corpus-by-corpus basis?
    # or should we insert data structures as is into the db?


