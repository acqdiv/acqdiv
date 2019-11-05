from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.yucatec.session_parser \
    import YucatecSessionParser


class YucatecCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return YucatecSessionParser(session_path)
