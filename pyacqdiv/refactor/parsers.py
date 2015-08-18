""" Parsers for CHAT XML and Toolbox files for acqdiv corpora, and an acqdiv config file parser.
"""

import os
import sys
import configparser
import glob
import re
import xml.etree.ElementTree as ET
import cree

from metadata import Imdi, Chat
from factories import *


# TODO: integrate the Corpus specific parsing routines from the body parser
# TODO: integrate the metadata parsing
from toolbox import ToolboxFile


class CorpusConfigParser(configparser.ConfigParser):
    """ Config parser for corpus .ini files """

    optionxform = str # preserves case

    # TODO: identify whether we want (extended) interolation, ordered dicts, inline commenting, etc.
#    _dict_type = collections.OrderedDict
#    _inline_comment_prefixes = ('#',)
#    _interpolation = configparser.ExtendedInterpolation()

#    def __init__(self, defaults=None):
#        super(Config, self).__init__(defaults, dict_type=self._dict_type,
#            inline_comment_prefixes=self._inline_comment_prefixes,
#            interpolation=self._interpolation)

    def __init__(self):
        super().__init__()

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

        if corpus == "Cree":
            return CreeParser(config, file_path)
        else:
            # print("Unknown Corpus. Defaulting...")
            if format == "ChatXML":
                return ChatXMLParser(config, file_path)
            if format == "Toolbox":
                return ToolboxParser(config, file_path)
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
    def next_record(self):
        pass

class ToolboxParser(SessionParser):
    """ For Chintang, Indonesian, Russian, & potentially Dene  """

    def __init__(self, config, file_path):
        SessionParser.__init__(self, config, file_path)

        # deal with the session body utterance, etc. data
        self.session_file = ToolboxFile(self.config, self.file_path)

        # deal with the metadata -- hack to get the separate metadata file paths for IMDIs
        # decision time: IMDI (Russian and Chintang) or XML (Indonesian)
        if self.config['metadata']['type'] == "XML":
            temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
            self.metadata_file_path = temp.replace(".txt", ".xml")
            self.metadata_parser = Chat(self.metadata_file_path)

        elif self.config['metadata']['type'] == "IMDI":
            temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
            self.metadata_file_path = temp.replace(".txt", ".imdi")
            self.metadata_parser = Imdi(self.metadata_file_path)

        else:
            assert 0, "Unknown format type: "#  + format


        # a check for missing metadata files
        """
        if not os.path.isfile(self.metadata_file_path):
            print("MISSING FILE:", self.metadata_file_path)
            sys.exit(1)
        """
        self.metadata_parser = Imdi(self.metadata_file_path)

    def get_session_metadata(self):
        # Do toolbox-specific parsing of session metadata.
        # Presumably we will have to look for the metadata file in the config.
        # The config so it knows what symbols to look for.
        return self.metadata_parser.metadata['session']

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

class ChatXMLParser(SessionParser):
    """ For Cree, Inuktitut, MiiPro, Miyata, Sesotho, Turkish, & Yucatec """

    def __init__(self, config, file_path):
        SessionParser.__init__(self, config, file_path)
        self.metadata_parser = Chat(self.file_path)
        #TODO: can this be a self.body_parser() or something?
        with open(self.file_path, 'r') as xml:
            self.tree = ET.parse(xml)
        self.root = self.tree.getroot()
        # this creates a dictionary of child:parent pairs
        # I don't know what it's good for yet but I'm putting it in here until
        # we can figure out what rsk uses it for in his parser
        # and whether we need it.
        self.pmap = {c:p for p in self.tree.iter() for c in p}
        self.clean_tree()

    def get_session_metadata(self):
        # Do xml-specific parsing of session metadata.
        # The config so it knows what symbols to look for.
        return self.metadata_parser.metadata['__attrs__']

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker

    def clean_tree(self):
        """ Removes prefixed namespaces """
        for elem in self.root.iter():
            elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
        #    tag = elem.tag
        #    attrib = elem.attrib
        #    #God knows what those are good for. Debugging?

    def next_utterance(self):
        # Do xml-specific parsing of utterances.
        # The config so it knows what symbols to look for.
        uf = XmlUtteranceFactory()

        for u in self.root.findall('.//u'):
            yield uf.make_utterance(u), uf.next_word, uf.next_morpheme
    
        # sample utterance processing call
        # ideally we'd just have to implement UtteranceFactory and be done here
        # also I supposed by "we" we mean "chysi"

class CreeParser(ChatXMLParser):

    def next_utterance(self):

        uf = cree.CreeUtteranceFactory()
        
        for u in self.root.findall('.//u'):
            yield uf.make_utterance(u), uf.next_word, uf.next_morpheme
