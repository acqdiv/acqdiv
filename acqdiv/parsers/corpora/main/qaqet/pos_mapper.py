import re

from acqdiv.parsers.toolbox.cleaners.morpheme_cleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.csvparser import parse_csv, parse_pos_ud
from acqdiv.util.path import get_full_path


class QaqetPOSMapper:

    pos_dict = parse_csv(get_full_path(
        'parsers/corpora/main/qaqet/resources/pos.csv'))

    pos_ud_dict = parse_pos_ud(get_full_path(
        'parsers/corpora/main/qaqet/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):

        if pos.startswith('-') or pos.startswith('='):
            return 'sfx'
        elif pos.endswith('-') or pos.endswith('='):
            return 'sfx'
        else:
            pos = cls.clean_pos(pos)

            if ud:
                return cls.pos_ud_dict.get(pos, '')
            else:
                return cls.pos_dict.get(pos, '')

    @classmethod
    def clean_pos(cls, pos):
        pos = cls.unify_unknowns_morpheme(pos)
        pos = ToolboxMorphemeCleaner.remove_morpheme_delimiters(pos)
        return pos

    @classmethod
    def unify_unknowns_morpheme(cls, morpheme):
        unknown_re = re.compile(r'\bx+|\?{2}|\*{3}')
        return unknown_re.sub('???', morpheme)
