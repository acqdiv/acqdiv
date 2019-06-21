from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.yucatec.YucatecReader import YucatecReader
from acqdiv.parsers.yucatec.YucatecCleaner import YucatecCleaner


class YucatecParser(CHATParser):
    @staticmethod
    def get_reader():
        return YucatecReader()

    @staticmethod
    def get_cleaner():
        return YucatecCleaner()
