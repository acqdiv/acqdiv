from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.nungon.NungonReader import NungonReader
from acqdiv.parsers.corpora.main.nungon.NungonCleaner import NungonCleaner


class NungonSessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return NungonReader(session_file)

    @staticmethod
    def get_cleaner():
        return NungonCleaner()
