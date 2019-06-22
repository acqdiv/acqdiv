from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.indonesian.IndonesianSessionParser \
    import IndonesianSessionParser


class IndonesianCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return IndonesianSessionParser(self.cfg, session_path)
