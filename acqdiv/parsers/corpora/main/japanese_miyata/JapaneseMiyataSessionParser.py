from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser
from acqdiv.parsers.corpora.main.japanese_miyata.JapaneseMiyataReader import \
    JapaneseMiyataReader
from acqdiv.parsers.corpora.main.japanese_miyata.JapaneseMiyataCleaner import \
    JapaneseMiyataCleaner


class JapaneseMiyataSessionParser(BaseCHATParser):
    @staticmethod
    def get_reader():
        return JapaneseMiyataReader()

    @staticmethod
    def get_cleaner():
        return JapaneseMiyataCleaner()
