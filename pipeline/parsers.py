""" Parsers for CHAT XML and Toolbox files for acqdiv corpora, and an acqdiv config file parser.
"""

import os
import sys
import configparser
import glob
import re
import xml.etree.ElementTree as ET
import json
import collections
from pprint import pprint

from metadata import Imdi, Chat

# TODO: integrate the Corpus specific parsing routines from the body parser
# TODO: integrate the metadata parsing
from toolbox import ToolboxFile


class CorpusConfigParser(configparser.ConfigParser):
    """ Config parser for corpus .ini files """

    def optionxform(self, optionstr):
        return optionstr


    # TODO: identify whether we want (extended) interolation, ordered dicts, inline commenting, etc.
    #    _dict_type = collections.OrderedDict
    #    _inline_comment_prefixes = ('#',)
    #    _interpolation = configparser.ExtendedInterpolation()

    #    def __init__(self, defaults=None):
    #        super(Config, self).__init__(defaults, dict_type=self._dict_type,
    #            inline_comment_prefixes=self._inline_comment_prefixes,
    #            interpolation=self._interpolation)

    def __init__(self):
        super().__init__(delimiters=["=="])

    # file level initializations    
    def read(self, filenames, encoding=None):
        super().read(filenames, encoding)

        # Load up the list of relative paths to corpus sessions files.
        # This creates a dependency that processors.py must be in same location as parsers.py!
        self.path = self['paths']['sessions']
        self.session_files = glob.glob(self.path)
        self.metadata_dir = self['paths']['metadata_dir']
        self.sessions_dir = self['paths']['sessions_dir']

        # Load up a dictionary of 'peculiarities'; these map the 'local'
        # symbols used in the corpus to the 'standard' symbols.
        # TODO: fix the inline commenting "#"
        # TODO: peculiarities moved to [record_tiers]
        # self.peculiarities = dict(self.items('peculiarities'))
        self.format = self['corpus']['format']
        self.corpus = self['corpus']['corpus']

        # ...And now any other additional things you want to do on
        # configfile load time.

class SessionParser(object):
    """ Static class-level method to create a new parser instance based on session format type.
    """

    @staticmethod
    def create_parser(config, file_path):
        corpus = config.corpus
        format = config.format

        # TODO: update when we dump using JSON
        if format == "ChatXML":
            if corpus == "Cree":
                return CreeParser(config, file_path)
            else:
                return ChatXMLParser(config, file_path)
        elif format == "Toolbox":
            return ToolboxParser(config, file_path)
        elif format == "JSON":
            return JsonParser(config, file_path)
        else:
            assert 0, "Unknown format type: " + format

    def __init__(self, config, file_path):
        self.config = config
        self.file_path = file_path
        # SessionParser.create_parser(self.config, self.file_path)

    # TODO: get SHA1 fingerprint of file -- provides unique data ID for db
    def sha1(self):
        pass

    # To be overridden in subclasses.
    # Session metadata for the Sessions table in the db
    def get_session_metadata(self):
        pass

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        pass

    # Generator to yield Utterances for the Utterance table in the db
    def next_utterance(self):
        pass

    # Generator to yield Utterances for the Utterance table in the db
    # def next_record(self):
    #    pass

class ToolboxParser(SessionParser):
    """ For Chintang, Indonesian, Russian, & potentially Dene  """

    def __init__(self, config, file_path):
        SessionParser.__init__(self, config, file_path)

        # Session body for utterances, etc.
        self.session_file = ToolboxFile(self.config, self.file_path)

        # Metadata
        if self.config['metadata']['type'] == "XML":
            # hack to get the separate metadata file paths for IMDIs
            temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
            self.metadata_file_path = temp.replace(".txt", ".xml")
            self.metadata_parser = Chat(self.config, self.metadata_file_path)

        elif self.config['metadata']['type'] == "IMDI":
            temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
            self.metadata_file_path = temp.replace(".txt", ".imdi")
            self.metadata_parser = Imdi(self.config, self.metadata_file_path)
        else:
            assert 0, "Unknown metadata format type: "#  + format


        # check for missing metadata files?
        """
        if not os.path.isfile(self.metadata_file_path):
            print("MISSING FILE:", self.metadata_file_path)
            sys.exit(1)
        """
        # self.metadata_parser = Imdi(self.metadata_file_path)

    def get_session_metadata(self):
        # Do toolbox-specific parsing of session metadata.
        # Presumably we will have to look for the metadata file in the config.
        # The config so it knows what symbols to look for.

        # TODO: fix this to just session or just __attrs__ in the metadata parser
        # this is an ugly hack due to the Indonesian corpus (body=Toolbox, but meta=XML)
        if self.metadata_parser.__class__.__name__ == "Imdi":
            return self.metadata_parser.metadata['session']
        elif self.metadata_parser.__class__.__name__ == "Chat":
            return self.metadata_parser.metadata['__attrs__']
        else:
            assert 0, "Unknown metadata format type: "#  + format

    def next_speaker(self):
        """ Yield participants metadata for the Speaker table in the db
        :return dictionary
        """
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker

    def next_utterance(self):
        """ Yield session level utterance data:
        returns ordered dictionary of config file record_tiers
        """
        for record in self.session_file:
            yield record

class JsonParser(SessionParser):
    """ Parser for JSON output from:
    https://github.com/uzling/acqdiv/tree/master/extraction/parsing

    # TODO:
        - what to do with the stars?
            - "phonetic": "* * *",
            - "phonetic_target": "* * *",

    """
    def __init__(self, config, file_path):
        SessionParser.__init__(self, config, file_path)

        # load the data
        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]
        with open(file_path) as data_file:
            self.data = json.load(data_file)
        # TODO: update when no longer using JSON
        temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
        self.metadata_file_path = temp.replace(".json", ".xml")
        self.metadata_parser = Chat(self.config, self.metadata_file_path)

    def next_utterance(self):
        """ Get each utterance from Robert's JSON output
        :return: utterance{}, words[word{}, word{}]
        """
        # Robert's JSON output is a dictionary: {key ("filename"): [u1{...}, u2{...}]}
        #  here we iterate over the utterances (each record)
        # Warning: the dictionary's key IS NOT ALWAYS the same as the file name...
        #  so we get the *key* (one json file per session; one key based on ID *or* filename)
        #  and use that, i.e. the source_id field
        x = self.data.keys() # in Py3 returns a dict_keys object, not a list!
        keys = list(x)
        assert(len(keys) == 1), "there is more than one key in the json file"
        key = keys[0] # should only be one top-level key per json file

        for record in self.data[key]:
            utterance = collections.OrderedDict()
            db_words = []
            morphemes = []

            # iterate over the utterance keys in the json parsed object and grab what is specified in the .ini
            for k in record:
                if k in self.config['json_mappings_utterance']:
                    label = self.config['json_mappings_utterance'][k]
                    utterance[label] = record[k]

                if k == 'words':
                    full_utterance = [] # Robert doesn't output the whole utterance, recreate it by gathering up the words
                    # Robert's {words:[]} is a list of dictionaries with keys like "full_word_target"
                    for word in record['words']:
                        d = collections.OrderedDict()
                        for k_json_mappings_words in self.config['json_mappings_words']:
                            if k_json_mappings_words in word and not type(word[k_json_mappings_words]) is dict:
                                d[self.config['json_mappings_words'][k_json_mappings_words]] = word[k_json_mappings_words]

                        # assign the proper actual vs target "word" given the corpus                        print(self.config['json_mappings_words']['word'])
                        # recreate the word utterance
                        if self.config['json_mappings_words']['word'] in d:
                            d['word'] = d[self.config['json_mappings_words']['word']]
                            full_utterance.append(d['word'])

                        # these are so awful -- only work because Robert alphabetically ordered the dictionary by keys
                        if 'utterance_id' in utterance:
                            d['utterance_id_fk'] = utterance['utterance_id']
                        if 'warnings' in word:
                            d[self.config['json_mappings_words']['warnings']] = word['warnings']

                        db_words.append(d)

                        # morphemes{} parsing within word[] and extraction of .ini specified db columns
                        # morphemes are also a key:[] pair in words{}; morphemes: [segment:'ga', pos_target:'Eng']...
                        if 'morphemes' in word:
                            segments = []
                            glosses = []
                            pos = []
                            d2 = collections.OrderedDict()
                            if len(word['morphemes']) > 0: # skip empty lists in the json
                                for e in word['morphemes']: # iter over morpheme dicts
                                    # i'm so ashamed here in the code...
                                    for k_json_mappings_morphemes in self.config['json_mappings_morphemes']:
                                        if k_json_mappings_morphemes in e and not type(e[k_json_mappings_morphemes]) is dict:
                                            d2[self.config['json_mappings_morphemes'][k_json_mappings_morphemes]] = \
                                            e[k_json_mappings_morphemes]
                                    if len(d2) > 0:
                                        morphemes.append(d2)
                                if 'segment_target' in d2:
                                    segments.append(d2['segment_target'])
                                if 'gloss_target' in d2:
                                    glosses.append(d2['gloss_target'])
                                if 'pos_target' in d2:
                                    pos.append(d2['pos_target'])

                            # this is so nasty hacky -- assumes all json files are the same!
                            if len(segments) > 0:
                                utterance['morpheme'] = " ".join(segments)
                            if len(pos) > 0:
                                utterance['pos'] = " ".join(pos)
                            if len(glosses) > 0:
                                utterance['gloss'] = " ".join(glosses)
                    # Recreate the full utterance string
                    utterance['utterance_raw'] = " ".join(full_utterance)
                    utterance['utterance'] = " ".join(full_utterance)
                    utterance['utterance_type'] = self.config['utterance']['type']
                    utterance['word'] = " ".join(full_utterance)
                    # TODO: add inference / clean-up
            yield utterance, db_words, morphemes

    # TODO: this will have to be removed (copied from ChatXML for the time being)
    def get_session_metadata(self):
        # Do xml-specific parsing of session metadata.
        # The config so it knows what symbols to look for.
        return self.metadata_parser.metadata['__attrs__']

    def next_speaker(self):
        """ Yield participants metadata for the Speaker table in the db
        :return dictionary
        """
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker


if __name__ == "__main__":
    import time
    start_time = time.time()

    from parsers import CorpusConfigParser
    cfg = CorpusConfigParser()
    cfg.read("CreeJSON.ini")
    f = "../../corpora/Cree/json/Ani/2006-10-18.json"  ## ATTN: the folder structure on the server looks different now: corpora/Cree/json/.json
    c = JsonParser(cfg, f)
    #c.next_utterance() # why doesn't this work?
    #because it's a generator and you really should be doing 
    next(c.next_utterance())
    #the original call creates a generator object, but doesn't do anything with it!
    print("\n--- %s seconds ---" % (time.time() - start_time))
