from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser
from acqdiv.parsers.corpora.main.sesotho.SesothoReader import SesothoReader
from acqdiv.parsers.corpora.main.sesotho.SesothoCleaner import SesothoCleaner


class SesothoSessionParser(BaseCHATParser):
    @staticmethod
    def get_reader():
        return SesothoReader()

    @staticmethod
    def get_cleaner():
        return SesothoCleaner()
