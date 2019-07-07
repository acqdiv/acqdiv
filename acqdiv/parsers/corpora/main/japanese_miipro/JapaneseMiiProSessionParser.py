from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProReader import \
    JapaneseMiiProReader
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner


class JapaneseMiiProSessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return JapaneseMiiProReader(session_file)

    @staticmethod
    def get_cleaner():
        return JapaneseMiiProCleaner()
