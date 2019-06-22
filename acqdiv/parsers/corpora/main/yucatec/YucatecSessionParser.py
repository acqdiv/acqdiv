from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser
from acqdiv.parsers.corpora.main.yucatec.YucatecReader import YucatecReader
from acqdiv.parsers.corpora.main.yucatec.YucatecCleaner import YucatecCleaner


class YucatecSessionParser(BaseCHATParser):
    @staticmethod
    def get_reader():
        return YucatecReader()

    @staticmethod
    def get_cleaner():
        return YucatecCleaner()
