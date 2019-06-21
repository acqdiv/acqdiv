from acqdiv.parsers.chat.CHATParser import PhonbankParser
from acqdiv.parsers.corpora.phonbank.quichua.QuichuaCleaner import \
    QuichuaCleaner
from acqdiv.parsers.corpora.phonbank.quichua.QuichuaReader import QuichuaReader


class QuichuaParser(PhonbankParser):

    @staticmethod
    def get_reader():
        return QuichuaReader()

    @staticmethod
    def get_cleaner():
        return QuichuaCleaner()