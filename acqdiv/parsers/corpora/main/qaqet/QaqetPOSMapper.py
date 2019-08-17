import re

from acqdiv.parsers.toolbox.cleaners.ToolboxMorphemeCleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class QaqetPOSMapper:

    pos_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/qaqet/resources/pos.csv'))

    pos_ud_dict = MorphemeMappingCSVParser.parse_pos_ud(
                    get_full_path(
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
