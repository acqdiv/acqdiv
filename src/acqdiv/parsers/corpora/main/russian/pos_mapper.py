from acqdiv.util.csvparser import parse_csv, parse_pos_ud
from acqdiv.util.path import get_full_path


class RussianPOSMapper:

    pos_dict = parse_csv(get_full_path(
        'parsers/corpora/main/russian/resources/pos.csv'))

    pos_ud_dict = parse_pos_ud(get_full_path(
        'parsers/corpora/main/russian/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
            if ud:
                return cls.pos_ud_dict.get(pos, '')
            else:
                return cls.pos_dict.get(pos, '')
