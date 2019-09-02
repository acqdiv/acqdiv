from acqdiv.parsers.chat.parser import CHATParser
from acqdiv.parsers.corpora.main.inuktitut.reader import \
    InuktitutReader
from acqdiv.parsers.corpora.main.inuktitut.cleaner import \
    InuktitutCleaner

from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path


class InuktitutSessionParser(CHATParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/inuktitut/resources/speaker_label2macro_role.csv'
    ))

    @staticmethod
    def get_reader(session_file):
        return InuktitutReader(session_file)

    @staticmethod
    def get_cleaner():
        return InuktitutCleaner()
