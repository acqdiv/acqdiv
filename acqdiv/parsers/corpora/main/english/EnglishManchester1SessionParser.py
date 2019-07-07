from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.english.EnglishManchester1Reader import \
    EnglishManchester1Reader
from acqdiv.parsers.corpora.main.english.EnglishManchester1Cleaner import \
    EnglishManchester1Cleaner


class EnglishManchester1SessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return EnglishManchester1Reader(session_file)

    @staticmethod
    def get_cleaner():
        return EnglishManchester1Cleaner()
