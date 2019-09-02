import re
from acqdiv.parsers.toolbox.cleaners.morpheme_cleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.csvparser import MorphemeMappingCSVParser
from acqdiv.util.path import get_full_path


class IndonesianGlossMapper:

    gloss_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/indonesian/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        gloss = ToolboxMorphemeCleaner.remove_morpheme_delimiters(gloss)
        return cls.gloss_dict.get(gloss, '')
