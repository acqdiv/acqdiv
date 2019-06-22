from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser
from acqdiv.parsers.corpora.main.turkish.TurkishReader import TurkishReader
from acqdiv.parsers.corpora.main.turkish.TurkishCleaner import TurkishCleaner


class TurkishSessionParser(BaseCHATParser):
    @staticmethod
    def get_reader():
        return TurkishReader()

    @staticmethod
    def get_cleaner():
        return TurkishCleaner()
