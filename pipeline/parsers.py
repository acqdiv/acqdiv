""" Parsers for CHAT XML and Toolbox files for acqdiv corpora, and an acqdiv config file parser.

TODO: integrate the Corpus specific parsing routines from the body parser
TODO: integrate the metadata parsing

"""

import os
import glob
import json
import collections
import configparser

from metadata import Imdi, Chat
from toolbox import ToolboxFile


class CorpusConfigParser(configparser.ConfigParser):
    """ Config parser for acqdiv corpus .ini files
    """

    def optionxform(self, optionstr):
        return optionstr

    def __init__(self):
        """ We subclass Python's default config parser and use our own delimiter
        """
        super().__init__(delimiters=["=="])

    def read(self, filenames, encoding=None):
        """ File level initializations

        Note: we assume processors.py is in the same location as parsers.py!

        Args:
            filenames: list of relative paths to corpus session files
            encoding: file encoding
        """
        super().read(filenames, encoding)
        self.path = self['paths']['sessions']
        self.session_files = glob.glob(self.path)
        self.metadata_dir = self['paths']['metadata_dir']
        self.sessions_dir = self['paths']['sessions_dir']
        self.format = self['corpus']['format']
        self.corpus = self['corpus']['corpus']


class SessionParser(object):
    """ Static class-level method to create a new parser instance based on session format type.
    """
    @staticmethod
    def create_parser(config, file_path):
        """ Factory method for creating a parser

        TODO: update logic below when we have an XML parser

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file

        Returns:
            A corpus-type-specific parser
        """
        corpus = config.corpus
        format = config.format

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
        """ Session parser initializer

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file
        """
        self.config = config
        self.file_path = file_path
        # SessionParser.create_parser(self.config, self.file_path)

    def sha1(self):
        # TODO: get SHA1 fingerprint of file -- provides unique data ID for db
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
    """ Toolbox parser for Chintang, Indonesian, Russian, & potentially Dene  """

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
        temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
        self.metadata_file_path = temp.replace(".json", ".xml")
        self.metadata_parser = Chat(self.config, self.metadata_file_path)

    def next_utterance(self):
        """ Get each utterance from Robert's JSON output

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
                    # Robert doesn't output the whole utterance, recreate it by gathering up the words
                    full_utterance = []
                    # Robert's {words:[]} is a list of dictionaries with keys like "full_word_target"
                    for word in record['words']:
                        d = collections.OrderedDict()
                        for k_json_mappings_words in self.config['json_mappings_words']:
                            if k_json_mappings_words in word and not type(word[k_json_mappings_words]) is dict:
                                d[self.config['json_mappings_words'][k_json_mappings_words]] = word[k_json_mappings_words]

                        # assign the proper actual vs target "word" given the corpus
                        # print(self.config['json_mappings_words']['word'])
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