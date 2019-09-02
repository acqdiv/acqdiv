import re

from acqdiv.parsers.chat.readers.reader import CHATReader
from acqdiv.parsers.corpora.main.turkish.gloss2segment_mapper \
    import TurkishGloss2SegmentMapper as Mp


class TurkishReader(CHATReader):

    def get_start_time(self):
        """Get the start time.

        It is located on the %tim tier.
        """
        time = self.record.dependent_tiers.get('tim', '')
        if not time:
            return ''
        else:
            time_regex = re.compile(r'([\d:]+)')
            return time_regex.search(time).group()

    def get_end_time(self):
        """Get the end time.

        It is located on the %tim tier and might be missing.
        """
        time = self.record.dependent_tiers.get('tim', '')
        if not time:
            return ''
        else:
            time_regex = re.compile(r'-([\d:]+)')
            match = time_regex.search(time)
            if match:
                return match.group(1)
            else:
                return ''

    def get_morph_tier(self):
        return self.record.dependent_tiers.get('xmor', '')

    @staticmethod
    def get_word_language(word):
        if word.endswith('@s:eng'):
            return 'English'
        elif word.endswith('@s:deu'):
            return 'German'
        elif word.endswith('@s:rus'):
            return 'Russian'
        else:
            return 'Turkish'

    @staticmethod
    def iter_morphemes(word):
        """Iter morphemes of a word.

        Morphemes are separated by dashes.

        Structure: stemPOS:substemPOS|stem-suffixgloss&subsuffixgloss

        Stem: segment, no gloss, POS tag
        Suffix: no segment, gloss, no POS tag (-> assign 'sfx')
        No prefixes, the first morpheme is always the stem.
        """
        morphemes = word.split('-')

        # first morpheme is always stem
        stem = morphemes.pop(0)

        # some morpheme words are malformed, null them
        if '|' not in stem:
            stem_seg = '???'
            stem_pos = '???'
        else:
            stem_pos, stem_seg = stem.split('|')

        yield stem_seg, '', stem_pos

        # iter suffixes
        for suffix in morphemes:
            segment = Mp.map(suffix)
            yield segment, suffix, 'sfx'

    @classmethod
    def get_segments(cls, seg_word):
        return [seg for seg, _, _ in cls.iter_morphemes(seg_word)]

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, gloss, _ in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, _, pos in cls.iter_morphemes(pos_word)]