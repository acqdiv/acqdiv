from acqdiv.parsers.chat.parser import CHATParser
from acqdiv.parsers.corpora.main.nungon.reader import NungonReader
from acqdiv.parsers.corpora.main.nungon.cleaner import NungonCleaner


class NungonSessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return NungonReader(session_file)

    @staticmethod
    def get_cleaner():
        return NungonCleaner()
