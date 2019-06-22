from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.dene.DeneSessionParser \
    import DeneSessionParser


class DeneCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return DeneSessionParser(self.cfg, session_path)
