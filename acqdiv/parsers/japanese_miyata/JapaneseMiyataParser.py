from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.japanese_miyata.JapaneseMiyataReader import \
    JapaneseMiyataReader
from acqdiv.parsers.japanese_miyata.JapaneseMiyataCleaner import \
    JapaneseMiyataCleaner


class JapaneseMiyataParser(CHATParser):
    @staticmethod
    def get_reader():
        return JapaneseMiyataReader()

    @staticmethod
    def get_cleaner():
        return JapaneseMiyataCleaner()
