from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser
from acqdiv.parsers.corpora.main.nungon.NungonReader import NungonReader
from acqdiv.parsers.corpora.main.nungon.NungonCleaner import NungonCleaner


class NungonSessionParser(BaseCHATParser):
    @staticmethod
    def get_reader():
        return NungonReader()

    @staticmethod
    def get_cleaner():
        return NungonCleaner()
