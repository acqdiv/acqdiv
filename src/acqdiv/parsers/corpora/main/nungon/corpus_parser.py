from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.nungon.session_parser \
    import NungonSessionParser


class NungonCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return NungonSessionParser(session_path)
