import re
from acqdiv.util.csvparser import parse_csv, parse_pos_ud
from acqdiv.util.path import get_full_path


class CreePOSMapper:

    pos_dict = parse_csv(get_full_path(
        'parsers/corpora/main/cree/resources/pos.csv'))

    pos_ud_dict = parse_pos_ud(get_full_path(
        'parsers/corpora/main/cree/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        pos = cls.clean_pos(pos)

        if ud:
            return cls.pos_ud_dict.get(pos, '')
        else:
            return cls.pos_dict.get(pos, '')

    @staticmethod
    def uppercase_pos_in_parentheses(pos):
        """Uppercase POS tags in parentheses.

        Parentheses indicate covert grammatical categories.
        """
        pos_in_parentheses_regex = re.compile(r'(\()(\S+)(\))')
        # extract POS in parentheses
        match = pos_in_parentheses_regex.search(pos)
        if not match:
            return pos
        else:
            # replace by uppercased version
            up_pos = match.group(2).upper()
            return pos_in_parentheses_regex.sub(r'\1{}\3'.format(up_pos), pos)

    @classmethod
    def clean_pos(cls, pos):
        return cls.uppercase_pos_in_parentheses(pos)
