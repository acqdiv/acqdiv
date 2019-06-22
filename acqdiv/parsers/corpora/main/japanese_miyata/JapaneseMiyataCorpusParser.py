from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.japanese_miyata.JapaneseMiyataSessionParser \
    import JapaneseMiyataSessionParser


class JapaneseMiyataCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return JapaneseMiyataSessionParser(session_path)
