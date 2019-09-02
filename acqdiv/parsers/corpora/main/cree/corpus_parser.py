from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.cree.session_parser \
    import CreeSessionParser


class CreeCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return CreeSessionParser(session_path)
