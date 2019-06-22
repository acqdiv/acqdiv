from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.cree.CreeSessionParser \
    import CreeSessionParser


class CreeCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return CreeSessionParser(session_path)
