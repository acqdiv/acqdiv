from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutReader import \
    InuktitutReader
from acqdiv.parsers.corpora.main.inuktitut.InuktitutCleaner import \
    InuktitutCleaner

from acqdiv.util.RoleMapper import RoleMapper
from acqdiv.util.util import get_full_path


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
