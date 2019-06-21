from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.japanese_miipro.JapaneseMiiProReader import \
    JapaneseMiiProReader
from acqdiv.parsers.japanese_miipro.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner


class JapaneseMiiProParser(CHATParser):
    @staticmethod
    def get_reader():
        return JapaneseMiiProReader()

    @staticmethod
    def get_cleaner():
        return JapaneseMiiProCleaner()
