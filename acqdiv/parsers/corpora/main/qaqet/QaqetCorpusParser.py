from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.qaqet.QaqetSessionParser \
    import QaqetSessionParser


class QaqetCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return QaqetSessionParser(self.cfg, session_path)
