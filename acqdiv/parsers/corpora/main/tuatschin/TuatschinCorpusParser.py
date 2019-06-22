from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.tuatschin.TuatschinSessionParser \
    import TuatschinSessionParser


class TuatschinCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return TuatschinSessionParser(self.cfg, session_path)
