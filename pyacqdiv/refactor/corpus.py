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
    corpus_name = "corpus"
    language = ""
    sessions = []
    # This should be a list of all sessions in the corpus
    # Its contents should be IDs, not actual session objects!

    def __init__(self,path):
        self.path = path

    def __sessions(self):
        # This should be a generator 
        # We want to yield a session object for processing at a time
        # Also, we need to build up a list of sessions in the corpus--
        # yield a tuple?
        pass


    # TODO:
    #  - define the common attributes across the corpora

class ChatXML(Corpus):
    name = ""

    # not sure here how @rabart extracts stuff from the XML, but Xpath
    #  seems reasonable; esp becuz you can get the patterns for free from
    #  the developer tools in some browsers

class Toolbox(Corpus):
    name = ""


