from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.turkish.TurkishReader import TurkishReader
from acqdiv.parsers.corpora.main.turkish.TurkishCleaner import TurkishCleaner


class TurkishSessionParser(CHATParser):
    @staticmethod
    def get_reader():
        return TurkishReader()

    @staticmethod
    def get_cleaner():
        return TurkishCleaner()
