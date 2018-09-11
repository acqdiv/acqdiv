""" Parsers for ACQDIV corpora, e.g. CHAT XML, Toolbox files
"""

import os
import json
import logging
import importlib
import configparser
from configparser import ExtendedInterpolation

from acqdiv.parsers.metadata import Chat
from acqdiv.parsers.xml_parser import XMLParserFactory

logger = logging.getLogger('pipeline.' + __name__)


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
        elif format == "cha":
            parser_module = importlib.import_module(
                'acqdiv.parsers.xml.CHATParser')
            parser_class = config['paths']['parser']
            parser = getattr(parser_module, parser_class)
            return parser
        elif format == "toolbox":
            parser_module = importlib.import_module(
                'acqdiv.parsers.ToolboxParser')
            parser_class = config['paths']['parser']
            parser = getattr(parser_module, parser_class)
            return lambda file_path: parser(config, file_path)
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
