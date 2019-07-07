from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.sesotho.SesothoReader import SesothoReader
from acqdiv.parsers.corpora.main.sesotho.SesothoCleaner import SesothoCleaner


class SesothoSessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return SesothoReader(session_file)

    @staticmethod
    def get_cleaner():
        return SesothoCleaner()
