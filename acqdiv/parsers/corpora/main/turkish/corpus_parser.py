from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.turkish.session_parser \
    import TurkishSessionParser


class TurkishCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return TurkishSessionParser(session_path)
