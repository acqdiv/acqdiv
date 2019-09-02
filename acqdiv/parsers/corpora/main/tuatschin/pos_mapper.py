import re

from acqdiv.util.csvparser import parse_csv, parse_pos_ud
from acqdiv.util.path import get_full_path


class TuatschinPOSMapper:

    pos_dict = parse_csv(get_full_path(
        'parsers/corpora/main/tuatschin/resources/pos.csv'))

    pos_ud_dict = parse_pos_ud(get_full_path(
        'parsers/corpora/main/tuatschin/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        pos = cls.clean_pos(pos)

        if ud:
            return cls.pos_ud_dict.get(pos, '')
        else:
            return cls.pos_dict.get(pos, '')

    @classmethod
    def clean_pos(cls, pos):
        for cleaning_method in [
            cls.remove_specifications
        ]:
            pos = cleaning_method(pos)
        return pos

    @staticmethod
    def remove_specifications(pos):
        """Remove specifications of POS tags.

        Specifications start with `_`.

        Examples:
        - words erroneously written apart: _cont
        - child forms: _Chld
        - discourse particles: _Discpart
        ...
        """
        regex = re.compile(r'_[^_]+')
        pos = regex.sub('', pos)
        return pos
