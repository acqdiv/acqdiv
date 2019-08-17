import re

from acqdiv.parsers.toolbox.cleaners.ToolboxMorphemeCleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class ChintangPOSMapper:

    pos_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/chintang/resources/pos.csv'))

    pos_ud_dict = MorphemeMappingCSVParser.parse_pos_ud(
                    get_full_path(
                        'parsers/corpora/main/chintang/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        if pos.startswith('-'):
            return 'sfx'
        elif pos.endswith('-'):
            return 'pfx'
        else:
            pos = ToolboxMorphemeCleaner.clean(pos)
            if ud:
                return cls.pos_ud_dict.get(pos, '')
            else:
                return cls.pos_dict.get(pos, '')
