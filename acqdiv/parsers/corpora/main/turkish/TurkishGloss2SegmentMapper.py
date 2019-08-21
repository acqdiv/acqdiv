from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser
from acqdiv.util.util import get_full_path


class TurkishGloss2SegmentMapper:

    gloss2seg = MorphemeMappingCSVParser.parse(get_full_path(
        'parsers/corpora/main/turkish/resources/gloss2segment.csv'))

    @classmethod
    def map(cls, gloss):
        return cls.gloss2seg.get(gloss, '')
