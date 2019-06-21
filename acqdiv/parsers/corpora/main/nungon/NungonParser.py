from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.nungon.NungonReader import NungonReader
from acqdiv.parsers.corpora.main.nungon.NungonCleaner import NungonCleaner


class NungonParser(CHATParser):
    @staticmethod
    def get_reader():
        return NungonReader()

    @staticmethod
    def get_cleaner():
        return NungonCleaner()
