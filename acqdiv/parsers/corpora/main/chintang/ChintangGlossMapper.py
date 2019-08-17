import re
from acqdiv.parsers.toolbox.cleaners.ToolboxMorphemeCleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class ChintangGlossMapper:

    gloss_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/chintang/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        gloss = ToolboxMorphemeCleaner.remove_morpheme_delimiters(gloss)
        return cls.gloss_dict.get(gloss, '')
