from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class JapaneseMiiProPOSMapper:

    pos_dict = MorphemeMappingCSVParser.parse(get_full_path(
                    'parsers/corpora/main/japanese_miipro/resources/pos.csv'))

    pos_ud_dict = MorphemeMappingCSVParser.parse_pos_ud(get_full_path(
                    'parsers/corpora/main/japanese_miipro/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        if ud:
            return cls.pos_ud_dict.get(pos, '')
        else:
            return cls.pos_dict.get(pos, '')
