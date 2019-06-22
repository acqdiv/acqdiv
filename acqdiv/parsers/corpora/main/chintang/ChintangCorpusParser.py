from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.chintang.ChintangSessionParser \
    import ChintangSessionParser


class ChintangCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return ChintangSessionParser(self.cfg, session_path)
