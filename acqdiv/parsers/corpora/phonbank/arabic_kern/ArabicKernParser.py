from acqdiv.parsers.chat.CHATParser import PhonbankParser
from acqdiv.parsers.corpora.phonbank.arabic_kern.ArabicKernCleaner import \
    ArabicKernCleaner
from acqdiv.parsers.corpora.phonbank.arabic_kern.ArabicKernReader import \
    ArabicKernReader


class ArabicKernParser(PhonbankParser):

    @staticmethod
    def get_reader():
        return ArabicKernReader()

    @staticmethod
    def get_cleaner():
        return ArabicKernCleaner()