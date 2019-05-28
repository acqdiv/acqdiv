
from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner


class JapaneseMiyataCleaner(CHATCleaner):

    # ---------- morphology tier cleaning ----------

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        morph_tier = cls.remove_terminator(morph_tier)
        return morph_tier

    # ---------- morphology tier cleaning ----------

    @classmethod
    def replace_colon_by_dot_pos(cls, pos):
        """Replace the colons in the POS tag by a dot."""
        return pos.replace(':', '.')

    @classmethod
    def clean_pos(cls, pos):
        pos = cls.replace_colon_by_dot_pos(pos)
        return pos

# ---------- utterance cross clean ----------

    @classmethod
    def utterance_cross_clean(
            cls, raw_utt, actual_utt, target_utt,
            seg_tier, gloss_tier, pos_tier):

        return JapaneseMiiProCleaner.utterance_cross_clean(
            raw_utt,
            actual_utt,
            target_utt,
            seg_tier,
            gloss_tier,
            pos_tier)
