from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProReader import \
    JapaneseMiiProReader
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner


class JapaneseMiiProSessionParser(BaseCHATParser):
    @staticmethod
    def get_reader():
        return JapaneseMiiProReader()

    @staticmethod
    def get_cleaner():
        return JapaneseMiiProCleaner()
