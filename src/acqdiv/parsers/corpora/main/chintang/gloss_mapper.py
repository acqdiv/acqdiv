from acqdiv.parsers.toolbox.cleaners.morpheme_cleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.csvparser import parse_csv
from acqdiv.util.path import get_full_path


class ChintangGlossMapper:

    gloss_dict = parse_csv(get_full_path(
                    'parsers/corpora/main/chintang/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        gloss = ToolboxMorphemeCleaner.remove_morpheme_delimiters(gloss)
        return cls.gloss_dict.get(gloss, '')
