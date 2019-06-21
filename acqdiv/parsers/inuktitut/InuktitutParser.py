from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.inuktitut.InuktitutReader import InuktitutReader
from acqdiv.parsers.inuktitut.InuktitutCleaner import InuktitutCleaner


class InuktitutParser(CHATParser):
    @staticmethod
    def get_reader():
        return InuktitutReader()

    @staticmethod
    def get_cleaner():
        return InuktitutCleaner()
