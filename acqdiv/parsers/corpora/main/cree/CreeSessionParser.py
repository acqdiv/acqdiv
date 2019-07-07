from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.cree.CreeReader import CreeReader
from acqdiv.parsers.corpora.main.cree.CreeCleaner import CreeCleaner


class CreeSessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return CreeReader(session_file)

    @staticmethod
    def get_cleaner():
        return CreeCleaner()
