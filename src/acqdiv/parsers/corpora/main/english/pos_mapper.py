from acqdiv.util.csvparser import parse_csv, parse_pos_ud
from acqdiv.util.path import get_full_path


class EnglishPOSMapper:

    pos_dict = parse_csv(get_full_path(
        'parsers/corpora/main/english/resources/pos.csv'))

    pos_ud_dict = parse_pos_ud(get_full_path(
        'parsers/corpora/main/english/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        pos = cls.clean_pos(pos)

        if ud:
            return cls.pos_ud_dict.get(pos, '')
        else:
            return cls.pos_dict.get(pos, '')

    @classmethod
    def clean_pos(cls, pos):
        return cls.extract_first_pos(pos)

    @staticmethod
    def extract_first_pos(pos):
        """Extract the first POS tag.

        Several POS tags are separated by ':'.
        """
        return pos.split(':')[0]
