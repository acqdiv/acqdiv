from acqdiv.parsers.toolbox.cleaners.ToolboxMorphemeCleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class KuWaruGlossMapper:

    gloss_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/ku_waru/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        return cls.gloss(gloss)

    @classmethod
    def gloss(cls, gloss):
        gloss = ToolboxMorphemeCleaner.clean(gloss)
        return cls.gloss_dict.get(gloss, '')
