from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.sesotho.session_parser \
    import SesothoSessionParser


class SesothoCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return SesothoSessionParser(session_path)
