from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.yucatec.YucatecReader import YucatecReader
from acqdiv.parsers.corpora.main.yucatec.YucatecCleaner import YucatecCleaner


class YucatecSessionParser(CHATParser):
    @staticmethod
    def get_reader(session_file):
        return YucatecReader(session_file)

    @staticmethod
    def get_cleaner():
        return YucatecCleaner()
