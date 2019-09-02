from acqdiv.util.csvparser import parse_csv
from acqdiv.util.path import get_full_path


class TurkishGloss2SegmentMapper:

    gloss2seg = parse_csv(get_full_path(
        'parsers/corpora/main/turkish/resources/gloss2segment.csv'))

    @classmethod
    def map(cls, gloss):
        return cls.gloss2seg.get(gloss, '')
