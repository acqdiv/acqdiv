from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProSessionParser \
    import JapaneseMiiProSessionParser


class JapaneseMiiProCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return JapaneseMiiProSessionParser(session_path)
