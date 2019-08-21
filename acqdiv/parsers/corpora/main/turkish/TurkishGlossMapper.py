from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class TurkishGlossMapper:

    gloss_dict = MorphemeMappingCSVParser.parse(
                    get_full_path(
                        'parsers/corpora/main/turkish/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        return cls.gloss_dict.get(gloss, '')
