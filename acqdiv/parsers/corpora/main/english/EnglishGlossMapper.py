from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class EnglishGlossMapper:

    gloss_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/english/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        return cls.gloss_dict.get(gloss, '')
