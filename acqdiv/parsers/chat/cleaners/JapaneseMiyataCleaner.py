
from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner


class JapaneseMiyataCleaner(CHATCleaner):

    # ---------- morphology tier cleaning ----------

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        morph_tier = cls.remove_terminator(morph_tier)
        return morph_tier
