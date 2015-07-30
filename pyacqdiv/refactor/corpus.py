import os
import re
import xml.etree.ElementTree as ET

from session import SessionLoader

""" Corpus objects for data extraction
"""

# read through each corpus folder
# grab all files
# logic for XML vs Toolbox

class CorpusProcessor(object):
    """ used to specify the corpus input files?
        cron-job? ;)
    """

class Corpus(object):
    # This should be a list of all sessions in the corpus
    # Its contents should be IDs, not actual session objects!

    def __init__(self, path, name, lang):
        self.path = path
        self.name = name
        self.language = lang
        self.sessions = []

    def __parse(self, fname):
        # This should contain the corpus-specific file parser
        return None

    def __process(self):
        # This should be the function that actually creates session objects
        return None

    def __sessions(self):
        # This should be a generator 
        # We want to yield a session object for processing at a time
        # Also, we need to build up a list of sessions in the corpus--
        # yield a tuple?

        sl = SessionLoader(self.__parse, self.__process, self.path)
        yield sl.sessions.next()

    def get_sessions(self):
        # Not quite sure if this is a useful interface but I figured I'd make a preliminary one
        return next(self.__sessions())

    # TODO:
    #  - define the common attributes across the corpora

class ChatXML(Corpus):

    def __init__(self, path, name, lang):
        super.__init__()

    def __parse(self, fname):
        with open(fp, 'r') as xml:
            tree = ET.parse(xml)
        return tree

    # not sure here how @rabart extracts stuff from the XML, but Xpath
    #  seems reasonable; esp becuz you can get the patterns for free from
    #  the developer tools in some browsers

class Toolbox(Corpus):
    
    def __init__(self, path, name, lang):
        super.__init__()

