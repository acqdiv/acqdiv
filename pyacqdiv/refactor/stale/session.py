import os
import re

class Session(object):
    """
    Session object for acqdiv corpora.
    """

    def __init__(self, data):
        pass

class SessionLoader(object):
    """
    Class to process the session objects contained in a corpus object.
    """

    def __init__(self, parse_func, proc_func, path):
        self.parse = parse_func
        self.process = proc_func
        self.path = path
        self.sessions = (Session(self.process(self.parse(f))) for f in os.walk(self.path))

