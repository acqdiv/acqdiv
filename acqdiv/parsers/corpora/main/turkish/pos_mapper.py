from acqdiv.util.csvparser import MorphemeMappingCSVParser
from acqdiv.util.path import get_full_path


class TurkishPOSMapper:

    pos_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/turkish/resources/pos.csv'))

    pos_ud_dict = MorphemeMappingCSVParser.parse_pos_ud(
                    get_full_path(
                        'parsers/corpora/main/turkish/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        if ud:
            return cls.pos_ud_dict.get(pos, '')
        else:
            return cls.pos_dict.get(pos, '')
