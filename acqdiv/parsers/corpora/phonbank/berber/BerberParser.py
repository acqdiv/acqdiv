from acqdiv.parsers.chat.CHATParser import PhonbankParser
from acqdiv.parsers.corpora.phonbank.berber.BerberCleaner import BerberCleaner
from acqdiv.parsers.corpora.phonbank.berber.BerberReader import BerberReader


class BerberParser(PhonbankParser):

    @staticmethod
    def get_reader():
        return BerberReader()

    @staticmethod
    def get_cleaner():
        return BerberCleaner()