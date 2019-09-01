from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.japanese_miyata.JapaneseMiyataReader import \
    JapaneseMiyataReader
from acqdiv.parsers.corpora.main.japanese_miyata.JapaneseMiyataCleaner import \
    JapaneseMiyataCleaner

from acqdiv.util.RoleMapper import RoleMapper
from acqdiv.util.util import get_full_path


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
