from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class InuktitutPOSMapper:

    pos_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/inuktitut/resources/pos.csv'))

    pos_ud_dict = MorphemeMappingCSVParser.parse_pos_ud(
                    get_full_path(
                        'parsers/corpora/main/inuktitut/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        pos = cls.clean_pos(pos)

        if ud:
            return cls.pos_ud_dict.get(pos, '')
        else:
            return cls.pos_dict.get(pos, '')

    @classmethod
    def clean_pos(cls, pos):
        """Replace the POS tag separator."""
        return cls.replace_pos_separator(pos)

    @staticmethod
    def replace_pos_separator(pos):
        """Replace the POS tag separator.

        A morpheme may have several POS tags separated by a pipe.
        POS tags to the right are subcategories of the POS tags to the left.
        The separator is replaced by a dot.

        Args:
            pos (str): The POS tag.

        Returns:
            str: POS tag separator replaced by a dot.
        """
        return pos.replace('|', '.')
