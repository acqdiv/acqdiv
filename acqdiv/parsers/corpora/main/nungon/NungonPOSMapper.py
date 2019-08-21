from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class NungonPOSMapper:

    pos_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/nungon/resources/pos.csv'))

    pos_ud_dict = MorphemeMappingCSVParser.parse_pos_ud(
                    get_full_path(
                        'parsers/corpora/main/nungon/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        pos = cls.remove_question_mark(pos)

        if ud:
            return cls.pos_ud_dict.get(pos, '')
        else:
            return cls.pos_dict.get(pos, '')

    @staticmethod
    def remove_question_mark(morpheme):
        """Remove the question mark in the morpheme.

        Question marks might code insecure annotations. They are prefixed to
        the morpheme.
        """
        return morpheme.lstrip('?')
