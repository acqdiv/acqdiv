from acqdiv.util.csvparser import parse_csv, parse_pos_ud
from acqdiv.util.path import get_full_path


class JapaneseMiyataPOSMapper:

    pos_dict = parse_csv(get_full_path(
                    'parsers/corpora/main/japanese_miyata/resources/pos.csv'))

    pos_ud_dict = parse_pos_ud(get_full_path(
                    'parsers/corpora/main/japanese_miyata/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        pos = cls.clean_pos(pos)
        if ud:
            return cls.pos_ud_dict.get(pos, '')
        else:
            return cls.pos_dict.get(pos, '')

    @classmethod
    def replace_colon_by_dot_pos(cls, pos):
        """Replace the colons in the POS tag by a dot."""
        return pos.replace(':', '.')

    @classmethod
    def clean_pos(cls, pos):
        pos = cls.replace_colon_by_dot_pos(pos)
        return pos
