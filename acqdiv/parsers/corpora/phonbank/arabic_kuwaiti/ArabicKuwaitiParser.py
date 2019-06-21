from acqdiv.parsers.chat.CHATParser import PhonbankParser
from acqdiv.parsers.corpora.phonbank.arabic_kuwaiti.ArabicKuwaitiCleaner import \
    ArabicKuwaitiCleaner
from acqdiv.parsers.corpora.phonbank.arabic_kuwaiti.ArabicKuwaitiReader import \
    ArabicKuwaitiReader


class ArabicKuwaitiParser(PhonbankParser):

    @staticmethod
    def get_reader():
        return ArabicKuwaitiReader()

    @staticmethod
    def get_cleaner():
        return ArabicKuwaitiCleaner()