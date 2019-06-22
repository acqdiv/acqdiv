from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.russian.RussianSessionParser \
    import RussianSessionParser


class RussianCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return RussianSessionParser(self.cfg, session_path)
