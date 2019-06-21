from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.english.EnglishManchester1Reader import \
    EnglishManchester1Reader
from acqdiv.parsers.english.EnglishManchester1Cleaner import \
    EnglishManchester1Cleaner


class EnglishManchester1Parser(CHATParser):
    @staticmethod
    def get_reader():
        return EnglishManchester1Reader()

    @staticmethod
    def get_cleaner():
        return EnglishManchester1Cleaner()
