import corpus
import session
import parselib

class AcqdivCreeCorpus(corpus.ChatXML):
    def __init__(self,path):
        super.__init__(self)

    def parse_corpus(self):
        yield s for s in self.get_sessions(self.path)

    def get_sessions(self):
        sessions = AcqdivCreeSessionLoader(self)

class AcqdivCreeSession(session.Session):
    def __init__(self,path):
        pass

class AcqdivCreeSessionLoader(session.SessionLoader):
    def __init__(self):
        pass
