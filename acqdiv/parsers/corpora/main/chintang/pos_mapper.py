from acqdiv.parsers.toolbox.cleaners.morpheme_cleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.csvparser import parse_csv, parse_pos_ud
from acqdiv.util.path import get_full_path


class ChintangPOSMapper:

    pos_dict = parse_csv(get_full_path(
        'parsers/corpora/main/chintang/resources/pos.csv'))

    pos_ud_dict = parse_pos_ud(get_full_path(
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
