from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.japanese_miyata.session_parser \
    import JapaneseMiyataSessionParser


class JapaneseMiyataCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return JapaneseMiyataSessionParser(session_path)
