""" Parsers for parsing CHAT XML and Toolbox files for acqdiv corpora
"""

import sys
import configparser
import glob
import xml.etree.ElementTree as ET

from metadata import Imdi, Chat
from factories import *


# TODO: integrate the Corpus specific parsing routines from the body parser
# TODO: integrate the metadata parsing


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
        self.peculiarities = dict(self.items('peculiarities'))
        self.format = self['corpus']['format']

        # ...And now any other additional things you want to do on
        # configfile load time.

class SessionParser(object):
    """ Static class-level method to create a new parser instance based on session format type. """

    @staticmethod
    def create_parser(config, file_path):
        format = config.format

        if format == "ChatXML":
            return ChatXMLParser(config, file_path)
        if format == "Toolbox":
            return ToolboxParser(config, file_path)
        assert 0, "Unknown format type: " + format

    def __init__(self, config, file_path):
        self.config = config
        self.file_path = file_path
        # SessionParser.create_parser(self.config, self.file_path)

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

class ToolboxParser(SessionParser):
    """ For Chintang, Indonesian, Russian, & Dene  """

    def __init__(self, config, file_path):
        SessionParser.__init__(self, config, file_path)
        # self.config = config
        # self.file = file

        # TODO: ugly hack -- fix
        temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
        self.metadata_file_path = temp.replace(".txt", ".imdi")

    # TODO: METADATA - call/integrate Cazim's metadata code and map it to the db tables
    # Note: make sure this is overriding the superclass.parse. Need a keyword?
    def get_session_metadata(self):
        # Do toolbox-specific parsing of session metadata.
        # Presumably we will have to look for the metadata file in the config.
        # The config so it knows what symbols to look for.

        metadata_file_path = ""
        imdi = Imdi(self.metadata_file_path)

        participants = imdi.get_participants()
        # print(type(participants))
        for i in participants:
            print(type(i), len(i))
        sys.exit(1)
        # return Imdi(self.file)

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        pass

    # Note: make sure this is overriding the superclass.parse. Need a keyword?
    def next_utterance(self):
        # Do toolbox-specific parsing of utterances.
        # The config so it knows what symbols to look for.
        pass

class ChatXMLParser(SessionParser):
    """ For Cree, Inuktitut, MiiPro, Miyata, Sesotho, Turkish, & Yucatec """

    def __init__(self, config, file):
        self.config = config
        self.file = file
        SessionParser.__init__(self, config, file)

    # TODO: METADATA - call/integrate Cazim's metadata code and map it to the db tables
    def __init__(self, config):
        super.__init__()
        self.fpath = self.config["file"]
        with open(self.fpath, 'r') as xml:
            self.tree = ET.parse(xml)
        self.root = self.tree.getroot()
        # this creates a dictionary of child:parent pairs
        # I don't know what it's good for yet but I'm putting it in here until
        # we can figure out what rsk uses it for in his parser
        # and whether we need it.
        self.pmap = {c:p for p in tree.iter() for c in p}
        self.clean_tree()

    def clean_tree(self):
        """ Removes prefixed namespaces """
        for elem in self.root.iter():
            elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
        #    tag = elem.tag
        #    attrib = elem.attrib
        #    #God knows what those are good for. Debugging?

    def get_session_metadata(self):
        # Do xml-specific parsing of session metadata.
        # The config so it knows what symbols to look for.
        pass

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        pass

    # Note: make sure this is overriding the superclass.parse. Need a keyword?
    def next_utterance(self):
        # Do xml-specific parsing of utterances.
        # The config so it knows what symbols to look for.
        uf = UtteranceFactory(self.config["utterance_config"])

        for u in self.root.findall('.//u'):
            yield uf.make_utterance(u)
    
        # sample utterance processing call
        # ideally we'd just have to implement UtteranceFactory and be done here
        # also I supposed by "we" we mean "chysi"

    # not sure here how @rabart extracts stuff from the XML, but Xpath
    #  seems reasonable; esp becuz you can get the patterns for free from
    #  the developer tools in some browsers
