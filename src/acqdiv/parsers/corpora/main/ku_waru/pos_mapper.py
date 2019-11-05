from acqdiv.parsers.toolbox.cleaners.morpheme_cleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.csvparser import parse_csv, parse_pos_ud
from acqdiv.util.path import get_full_path


class KuWaruPOSMapper:

    pos_dict = parse_csv(get_full_path(
        'parsers/corpora/main/ku_waru/resources/pos.csv'))

    pos_ud_dict = parse_pos_ud(get_full_path(
        'parsers/corpora/main/ku_waru/resources/pos.csv'))

    @classmethod
    def map(cls, pos, ud=False):
        if ud:
            return cls.infer_pos(pos, cls.pos_ud_dict)
        else:
            return cls.infer_pos(pos, cls.pos_dict)

    @classmethod
    def infer_pos(cls, pos, pos_dict):
        if cls.is_suffix(pos):
            return 'sfx'
        elif cls.is_prefix(pos):
            return 'pfx'
        else:
            pos = ToolboxMorphemeCleaner.clean(pos)
            return pos_dict.get(pos, '')

    @staticmethod
    def is_suffix(pos):
        return pos.startswith('-') or pos.startswith('=')

    @staticmethod
    def is_prefix(pos):
        return pos.endswith('-') or pos.endswith('=')
