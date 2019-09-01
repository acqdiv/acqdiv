from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.cree.CreeReader import CreeReader
from acqdiv.parsers.corpora.main.cree.CreeCleaner import CreeCleaner

from acqdiv.util.RoleMapper import RoleMapper
from acqdiv.util.util import get_full_path


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
