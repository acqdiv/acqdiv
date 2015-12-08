import re
import collections.abc as abc
from parsers import CorpusConfigParser as ccp
from lxml import etree

class ChatXMLFile(abc.Iterable):

    def __init__(self, cfg, filepath):
        self.config = ccp().read(cfg)
        self.__filepath = filepath

    def __iter__(self):
        pass

class XMLParser(object):
    pass

class CreeParser(XMLParser):
    pass
