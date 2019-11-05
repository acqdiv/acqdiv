from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.english.session_parser \
    import EnglishManchester1SessionParser


class EnglishCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return EnglishManchester1SessionParser(session_path)
