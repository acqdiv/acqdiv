from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.yucatec.YucatecSessionParser \
    import YucatecSessionParser


class YucatecCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return YucatecSessionParser(session_path)
