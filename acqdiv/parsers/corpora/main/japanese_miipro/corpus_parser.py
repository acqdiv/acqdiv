from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.japanese_miipro.session_parser \
    import JapaneseMiiProSessionParser


class JapaneseMiiProCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return JapaneseMiiProSessionParser(session_path)
