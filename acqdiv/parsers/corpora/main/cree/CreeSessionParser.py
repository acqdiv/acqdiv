from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser
from acqdiv.parsers.corpora.main.cree.CreeReader import CreeReader
from acqdiv.parsers.corpora.main.cree.CreeCleaner import CreeCleaner


class CreeSessionParser(BaseCHATParser):
    @staticmethod
    def get_reader():
        return CreeReader()

    @staticmethod
    def get_cleaner():
        return CreeCleaner()
