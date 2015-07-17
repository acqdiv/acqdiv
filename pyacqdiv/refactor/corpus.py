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

    # TODO:
    #  - define the common attributes across the corpora

class ChatXML(Corpus):
    name = ""

    # not sure here how @rabart extracts stuff from the XML, but Xpath
    #  seems reasonable; esp becuz you can get the patterns for free from
    #  the developer tools in some browsers

class Toolbox(Corpus):
    name = ""


