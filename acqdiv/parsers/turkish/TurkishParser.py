from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.turkish.TurkishReader import TurkishReader
from acqdiv.parsers.turkish.TurkishCleaner import TurkishCleaner


class TurkishParser(CHATParser):
    @staticmethod
    def get_reader():
        return TurkishReader()

    @staticmethod
    def get_cleaner():
        return TurkishCleaner()
