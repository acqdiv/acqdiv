from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.inuktitut.session_parser \
    import InuktitutSessionParser


class InuktitutCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return InuktitutSessionParser(session_path)
