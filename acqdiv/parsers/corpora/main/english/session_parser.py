from acqdiv.parsers.chat.parser import CHATParser
from acqdiv.parsers.corpora.main.english.reader import \
    EnglishManchester1Reader
from acqdiv.parsers.corpora.main.english.cleaner import \
    EnglishManchester1Cleaner


class EnglishManchester1SessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return EnglishManchester1Reader(session_file)

    @staticmethod
    def get_cleaner():
        return EnglishManchester1Cleaner()
