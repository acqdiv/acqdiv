from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.cree.CreeReader import CreeReader
from acqdiv.parsers.corpora.main.cree.CreeCleaner import CreeCleaner


class CreeParser(CHATParser):
    @staticmethod
    def get_reader():
        return CreeReader()

    @staticmethod
    def get_cleaner():
        return CreeCleaner()
