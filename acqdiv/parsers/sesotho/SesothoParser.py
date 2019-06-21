from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.sesotho.SesothoReader import SesothoReader
from acqdiv.parsers.sesotho.SesothoCleaner import SesothoCleaner


class SesothoParser(CHATParser):
    @staticmethod
    def get_reader():
        return SesothoReader()

    @staticmethod
    def get_cleaner():
        return SesothoCleaner()
