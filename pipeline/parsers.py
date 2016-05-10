""" Parsers for ACQDIV corpora, e.g. CHAT XML, Toolbox files
"""

import os
import sys
import glob
import json
import collections
import configparser
from configparser import ExtendedInterpolation
from collections import namedtuple

from metadata import Imdi, Chat
from toolbox import ToolboxFile
from xml_parser import XMLParserFactory


class CorpusConfigParser(configparser.ConfigParser):
    """ Config parser for ACQDIV corpus-specific .ini configuration files
    """
    def optionxform(self, optionstr):
        return optionstr

    def __init__(self):
        """ We subclass Python's default config parser and use our own delimiter and extended interpolation.
        """
        super().__init__(delimiters=["=="], interpolation=ExtendedInterpolation())

    def read(self, config, encoding=None):
        super().read(config, encoding)


class SessionParser(object):
    """ Static class-level method to create a new parser instance based on session format type.
    """
    def __init__(self, config, file_path):
        """ Session parser initializer

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file
        """
        self.config = config
        self.file_path = file_path

    @staticmethod
    def create_parser_factory(config):
        """ Factory method for creating a corpus session parser based on input format type (e.g. Toolbox, ChatXML).

        Args:
            config: CorpusConfigParser

        Returns:
            A corpus-type-specific parser
        """
        format = config['corpus']['format']

        if format == "xml":
            return XMLParserFactory(config)
        elif format == "toolbox":
            return lambda file_path: ToolboxParser(config, file_path)
        elif format == "json":
            return lambda file_path: JsonParser(config, file_path)
        else:
            assert 0, "Unknown format type: " + format

    def get_sha1(self):
        # TODO: get SHA1 fingerprint for each session file and write to the sessions table.
        pass

    def get_session_metadata(self):
        """ Gets session metadata for the Sessions table in the db
        """
        pass

    def next_speaker(self):
        """ Yield speakers for the Speaker table in the db
        """
        pass

    def next_utterance(self):
        """ Yield utterances for the Utterance table in the db
        """
        pass

    # Generator to yield Utterances for the Utterance table in the db
    # def next_record(self):
    #    pass


class ToolboxParser(SessionParser):
    """ Toolbox parser for Chintang, Indonesian, Russian, & potentially Dene
    """
    def __init__(self, config, file_path):
        """ Initialize a Toolbox parser

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file

        Returns:
            A Toolbox parser
        """
        SessionParser.__init__(self, config, file_path)

        # Session body for utterances, etc.
        self.session_file = ToolboxFile(self.config, self.file_path)

        # Metadata
        if self.config['metadata']['type'] == "xml":
            # Hack to get the separate metadata file paths for IMDIs
            temp = self.file_path.replace(self.config['paths']['sessions_dir'], self.config['paths']['metadata_dir'])
            self.metadata_file_path = temp.replace(".txt", ".xml")
            self.metadata_parser = Chat(self.config, self.metadata_file_path)
        elif self.config['metadata']['type'] == "imdi":
            temp = self.file_path.replace(self.config['paths']['sessions_dir'], self.config['paths']['metadata_dir'])
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
        """ Do toolbox-specific parsing of session metadata

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file

        Returns:
            Session metadata
        """
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

        Returns:
            Ordered dictionary of speaker (participant) metadata
        """
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker

    def next_utterance(self):
        """ Yield session level utterance data:

        Returns:
             Ordered dictionary of config file record_tiers
        """
        for record in self.session_file:
            if record is None:
                raise StopIteration
            yield record


class JsonParser(SessionParser):
    """ Parser for JSON output
    # TODO: what to do with the stars, e.g. "phonetic": "* * *", "phonetic_target": "* * *"
    """
    def __init__(self, config, file_path):
        """ Initialize a JsonParser

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file

        Returns:
            A JsonParser
        """
        SessionParser.__init__(self, config, file_path)
        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]
        with open(file_path) as data_file:
            self.data = json.load(data_file)
        temp = self.file_path.replace(self.config['paths']['sessions_dir'], self.config['paths']['metadata_dir'])
        self.metadata_file_path = temp.replace(".json", ".xml")
        self.metadata_parser = Chat(self.config, self.metadata_file_path)

    def next_utterance(self):
        """ Get utterance, words and morphemes from Robert's JSON output

        Notes:
            Robert's JSON output is a dictionary: {key ("filename"): [u1{...}, u2{...}]}. Here we iterate over the
            utterances (each record).
            Warning: the dictionary's key IS NOT ALWAYS the same as the file name, so we get the *key* (one json
            file per session; one key based on ID *or* filename) and use that, i.e. the source_id field.

        Returns:
            utterance{}, words[word{}, word{}]
        """
        x = self.data.keys() # in Py3 returns a dict_keys object, not a list!
        keys = list(x)
        assert(len(keys) == 1), "there is more than one key in the json file"
        key = keys[0] # should only be one top-level key per json file

        # TODO: config session label mapping replacement afterwards
        for record in self.data[key]:
            utterance = {}
            words = []
            morphemes = []

            # take only the config specified fields
            for k, v in record.items():
                if k in self.config['json_mappings']:
                    utterance[self.config['json_mappings'][k]] = v.strip()

            # get initial words and morphemes
            if 'words' in record and not len(record['words']) == 0:
                for word in record['words']:
                    words.append(word)
                    if 'morphemes' in word:
                        morphemes.append(word['morphemes'])

            # take only the config specified fields
            temp = []
            full_utterance = [] # utterance reconstruction
            for word in words:
                d = {}
                for k, v in word.items():
                    if k in self.config['json_mappings']:
                        d[self.config['json_mappings'][k]] = v.strip()
                temp.append(d)
                # full utterance re-creation and populate words.word
                if self.config['json_mappings']['word'] in d:
                    full_utterance.append(d[self.config['json_mappings']['word']])
                    d['word'] = d[self.config['json_mappings']['word']]

            utterance['utterance_raw'] = " ".join(full_utterance)
            utterance['utterance'] = " ".join(full_utterance)
            words = temp

            # take only the config specified fields
            temp = []
            for i in morphemes: # [[{},{}], [{}]]
                temp2 = []
                # reconstructions:
                morpheme = []
                gloss = []
                pos = []

                for j in i: # [{},{}]
                    d = {}
                    for k, v in j.items():
                        if k in self.config['json_mappings']:
                           d[self.config['json_mappings'][k]] = v.strip()
                    temp2.append(d)
                    # reconstructions: # TODO: add words, segments, etc.
                    if 'morpheme' in d:
                        morpheme.append(d['morpheme'])
                    if 'gloss_raw' in d:
                        gloss.append(d['gloss_raw'])
                    if 'pos_raw' in d:
                        pos.append(d['pos_raw'])

                temp.append(temp2)
                # reconstructions
                utterance['morpheme'] = " ".join(morpheme)
                utterance['gloss_raw'] = " ".join(gloss)
                utterance['pos_raw'] = " ".join(pos)
            morphemes = temp
            yield utterance, words, morphemes


    def get_session_metadata(self):
        """ Do xml-specific parsing of session metadata.

        Returns:
            Ordered dictionary of session metadata
        """
        return self.metadata_parser.metadata['__attrs__']


    def next_speaker(self):
        """ Yield participants metadata for the Speaker table in the db

        Returns:
             Ordered dictionary of speaker metadata
        """
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker
