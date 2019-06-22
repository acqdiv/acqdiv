from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.turkish.TurkishSessionParser \
    import TurkishSessionParser


class TurkishCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return TurkishSessionParser(session_path)
