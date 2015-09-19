import codecs
import collections
import os
import re
import xml.etree.ElementTree as ET

class WordParser(dict):
    def __init__(self):
        super.__init__()

class UtteranceParser(object):
    def __init__(self):
        self.data = self.load_utterance(self)
        self.words = self.get_words(self)

    def load_utterance(self):
        pass

    def get_words(self):
        pass

class SessionParser(object):
    def __init__(self):
        self.data = self.load_session(self)
        self.utterances = self.get_utterances(self)

    def load_session(self):
        pass

    def get_utterances(self):
        pass

class CorpusParser(object):
    def __init__(self, path, lang):
        self.path = path
        self.data = self.load_corpus(self)
        self.sessions = self.corpus.get_sessions(self)
        
    def load_corpus(self):
        pass

    def get_sessions(self):
       pass
