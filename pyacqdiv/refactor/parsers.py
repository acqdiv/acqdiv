""" Parsers for parsing CHAT XML and Toolbox files for acqdiv corpora
"""

import sys
import xml.etree.ElementTree as ET
from factories import *

# TODO: integrate the Corpus specific parsing routines from the body parser
# TODO: integrate the metadata parsing

class SessionParser(object):
    # Static class-level method to create a new parser instance
    # based on session format type.
    @staticmethod
    def create_parser(config, file):
        format = config['corpus']['format']

        if format == "ChatXML":
            return ChatXMLParser(config)
        if format == "Toolbox":
            return ToolboxParser(config)
        assert 0, "Unknown format type: " + format
    # create_parser(config) = staticmethod(create_parser)

    def __init__(self, config):
        self.config = config

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
    """ Chintang, Indonesian, Russian, Dene
    """
    # Note: do we need additional special syntax to indicate that we're extending Session?

    # TODO: METADATA - call/integrate Cazim's metadata code and map it to the db tables
    # Note: make sure this is overriding the superclass.parse. Need a keyword?
    def get_session_metadata(self):
        # Do toolbox-specific parsing of session metadata.
        # Presumably we will have to look for the metadata file in the config.
        # The config so it knows what symbols to look for.
        pass

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        pass

    # Note: make sure this is overriding the superclass.parse. Need a keyword?
    def next_utterance(self):
        # Do toolbox-specific parsing of utterances.
        # The config so it knows what symbols to look for.
        pass

class ChatXMLParser(SessionParser):
    """ Cree, Inuktitut, MiiPro, Miyata, Sesotho, Turkish, Yucatec
    """
    # Note: do we need additional special syntax to indicate that we're extending Session?

    # TODO: METADATA - call/integrate Cazim's metadata code and map it to the db tables
    # Note: make sure this is overriding the superclass.parse. Need a keyword?

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
        """
        Removes prefixed namespaces
        """
        
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
