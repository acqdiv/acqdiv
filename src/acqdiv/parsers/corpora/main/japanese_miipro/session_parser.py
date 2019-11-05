from acqdiv.parsers.chat.parser import CHATParser
from acqdiv.parsers.corpora.main.japanese_miipro.reader import \
    JapaneseMiiProReader
from acqdiv.parsers.corpora.main.japanese_miipro.cleaner import \
    JapaneseMiiProCleaner

from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path


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
