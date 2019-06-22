from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutReader import \
    InuktitutReader
from acqdiv.parsers.corpora.main.inuktitut.InuktitutCleaner import \
    InuktitutCleaner


class InuktitutSessionParser(BaseCHATParser):
    @staticmethod
    def get_reader():
        return InuktitutReader()

    @staticmethod
    def get_cleaner():
        return InuktitutCleaner()
