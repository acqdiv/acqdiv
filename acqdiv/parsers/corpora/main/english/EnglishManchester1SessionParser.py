from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser
from acqdiv.parsers.corpora.main.english.EnglishManchester1Reader import \
    EnglishManchester1Reader
from acqdiv.parsers.corpora.main.english.EnglishManchester1Cleaner import \
    EnglishManchester1Cleaner


class EnglishManchester1SessionParser(BaseCHATParser):
    @staticmethod
    def get_reader():
        return EnglishManchester1Reader()

    @staticmethod
    def get_cleaner():
        return EnglishManchester1Cleaner()
