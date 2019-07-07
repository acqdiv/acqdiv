from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutReader import \
    InuktitutReader
from acqdiv.parsers.corpora.main.inuktitut.InuktitutCleaner import \
    InuktitutCleaner


class InuktitutSessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return InuktitutReader(session_file)

    @staticmethod
    def get_cleaner():
        return InuktitutCleaner()
