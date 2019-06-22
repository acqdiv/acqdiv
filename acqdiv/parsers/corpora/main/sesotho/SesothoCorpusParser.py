from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.sesotho.SesothoSessionParser \
    import SesothoSessionParser


class SesothoCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return SesothoSessionParser(session_path)
