from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.english.EnglishManchester1SessionParser \
    import EnglishManchester1SessionParser


class EnglishCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return EnglishManchester1SessionParser(session_path)
