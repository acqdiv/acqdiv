from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.nungon.NungonSessionParser \
    import NungonSessionParser


class NungonCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return NungonSessionParser(session_path)
