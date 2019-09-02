from acqdiv.parsers.chat.readers.reader import CHATReader


class CreeReader(CHATReader):

    @staticmethod
    def get_main_morpheme():
        return 'segment'

    def get_seg_tier(self):
        return self.record.dependent_tiers.get('xtarmor', '')

    def get_gloss_tier(self):
        return self.record.dependent_tiers.get('xmormea', '')

    def get_pos_tier(self):
        return self.record.dependent_tiers.get('xmortyp', '')

    @staticmethod
    def get_morphemes(word):
        if word:
            return word.split('~')
        else:
            return []

    @classmethod
    def get_segments(cls, seg_word):
        return cls.get_morphemes(seg_word)

    @classmethod
    def get_glosses(cls, gloss_word):
        return cls.get_morphemes(gloss_word)

    @classmethod
    def get_poses(cls, pos_word):
        return cls.get_morphemes(pos_word)

    @staticmethod
    def get_morpheme_language(seg, gloss, pos):
        if gloss == 'Eng':
            return 'English'
        else:
            return 'Cree'
