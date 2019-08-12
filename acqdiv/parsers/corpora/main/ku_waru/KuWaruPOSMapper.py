import re

from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class KuWaruPOSMapper:

    pos_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/ku_waru/resources/pos.csv'))

    @classmethod
    def infer_pos(cls, pos):
        if pos.startswith('-') or pos.startswith('='):
            return 'sfx'
        elif pos.endswith('-') or pos.endswith('='):
            return 'pfx'
        elif pos in ['']:
            return pos
        else:
            pos = cls.remove_morpheme_delimiters(pos)
            pos = cls.unify_unknown(pos)
            return cls.pos_dict.get(pos, '')

    @staticmethod
    def remove_morpheme_delimiters(pos):
        """Remove morpheme delimiters.

        Morpheme delimiters are `-` and `=`.
        """
        return pos.replace('-', '').replace('=', '')

    @staticmethod
    def unify_unknown(pos):
        return re.sub(r'\*{3}|\?{3}', '', pos)

    @classmethod
    def map(cls, pos):
        return cls.infer_pos(pos)
