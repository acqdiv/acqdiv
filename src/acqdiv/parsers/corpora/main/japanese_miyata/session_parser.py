from acqdiv.parsers.chat.parser import CHATParser
from acqdiv.parsers.corpora.main.japanese_miyata.reader import \
    JapaneseMiyataReader
from acqdiv.parsers.corpora.main.japanese_miyata.cleaner import \
    JapaneseMiyataCleaner

from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path


class JapaneseMiyataSessionParser(CHATParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/japanese_miyata/resources/'
        'speaker_label2macro_role.csv'
    ))

    @staticmethod
    def get_reader(session_file):
        return JapaneseMiyataReader(session_file)

    @staticmethod
    def get_cleaner():
        return JapaneseMiyataCleaner()
