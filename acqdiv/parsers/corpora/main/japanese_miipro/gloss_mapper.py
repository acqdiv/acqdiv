from acqdiv.util.csvparser import MorphemeMappingCSVParser
from acqdiv.util.path import get_full_path


class JapaneseMiiProGlossMapper:

    gloss_dict = MorphemeMappingCSVParser.parse(get_full_path(
                'parsers/corpora/main/japanese_miipro/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        return cls.gloss_dict.get(gloss, '')
