from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProReader import \
    JapaneseMiiProReader
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner

from acqdiv.util.RoleMapper import RoleMapper
from acqdiv.util.util import get_full_path


class JapaneseMiiProSessionParser(CHATParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/japanese_miipro/resources/'
        'speaker_label2macro_role.csv'
    ))

    @staticmethod
    def get_reader(session_file):
        return JapaneseMiiProReader(session_file)

    @staticmethod
    def get_cleaner():
        return JapaneseMiiProCleaner()
