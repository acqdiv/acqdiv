from acqdiv.util.csvparser import MorphemeMappingCSVParser
from acqdiv.util.path import get_full_path


class JapaneseMiyataGloss2SegmentMapper:

    gloss2seg = MorphemeMappingCSVParser.parse(get_full_path(
        'parsers/corpora/main/japanese_miyata/resources/gloss2segment.csv'))

    @classmethod
    def map(cls, gloss):
        return cls.gloss2seg.get(gloss, '')
