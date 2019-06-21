from acqdiv.parsers.chat.CHATParser import PhonbankParser
from acqdiv.parsers.corpora.phonbank.polish.PolishCleaner import PolishCleaner
from acqdiv.parsers.corpora.phonbank.polish.PolishReader import PolishReader


class PolishParser(PhonbankParser):

    @staticmethod
    def get_reader():
        return PolishReader()

    @staticmethod
    def get_cleaner():
        return PolishCleaner()