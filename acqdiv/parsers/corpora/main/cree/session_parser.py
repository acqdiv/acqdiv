from acqdiv.parsers.chat.parser import CHATParser
from acqdiv.parsers.corpora.main.cree.reader import CreeReader
from acqdiv.parsers.corpora.main.cree.cleaner import CreeCleaner

from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path


class CreeSessionParser(CHATParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/cree/resources/speaker_label2macro_role.csv'
    ))

    @staticmethod
    def get_reader(session_file):
        return CreeReader(session_file)

    @staticmethod
    def get_cleaner():
        return CreeCleaner()
