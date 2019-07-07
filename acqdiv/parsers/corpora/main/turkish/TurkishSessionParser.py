from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.turkish.TurkishReader import TurkishReader
from acqdiv.parsers.corpora.main.turkish.TurkishCleaner import TurkishCleaner


class TurkishSessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return TurkishReader(session_file)

    @staticmethod
    def get_cleaner():
        return TurkishCleaner()
