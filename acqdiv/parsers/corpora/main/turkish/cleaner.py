import re

from acqdiv.parsers.chat.cleaners.cleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.utterance_cleaner \
    import CHATUtteranceCleaner
from acqdiv.parsers.corpora.main.turkish.gloss_mapper \
    import TurkishGlossMapper
from acqdiv.parsers.corpora.main.turkish.pos_mapper \
    import TurkishPOSMapper


class TurkishCleaner(CHATCleaner):

    @staticmethod
    def clean_name(name):
        if name == 'Unknown':
            return ''
        else:
            return name

    # ---------- morphology tier cleaning ----------

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        return CHATUtteranceCleaner.remove_terminator(morph_tier)

    # ---------- cross cleaning ----------

    @staticmethod
    def single_morph_word(utterance, morph_tier):
        """Handle complexes consisting of a single morphological word.

        A complex consists of several stems that are either joined by + or _.

        A complex is a single morphological word, if it has a single POS tag.
        The orthographic word will be joined by an underscore. Example:
        POS|stem1_stem2-SFX
        word:
            seg = stem1_stem2   gloss = ??? pos = POS
            seg = ???           gloss = SFX pos = ???
        """
        wwords = utterance.split(' ')
        mwords = morph_tier.split(' ')
        wwords_count = len(wwords)
        mwords_count = len(mwords)

        i = 0
        while i < wwords_count and i < mwords_count:
            mword = mwords[i]
            wword = wwords[i]
            if '_' in mword or '+' in mword:
                if '_' not in wword and '+' not in wword:
                    # check if wword and mword are similar (-> misalignment)
                    if wword[:2] in mword:
                        # check if there is a next word (-> missing join sep)
                        if i + 1 < wwords_count:
                            next_word = wwords[i+1]
                            # check if wword and mword are similar
                            if next_word[:2] in mword:
                                del wwords[i+1]
                                wwords[i] += '_' + next_word
                                wwords_count -= 1
            i += 1

        return ' '.join(wwords), morph_tier

    @staticmethod
    def separate_morph_word(utterance, morph_tier):
        """Handle complexes consisting of separate morphological words.

        A complex consists of several stems that are either joined by + or _.

        A complex consists of two morphological words, if it has separate
        POS tags and suffixes. The orthographic word as well as the
        morphological word is split in this case. The POS tag of the whole
        complex is discarded. Example:
        wholePOS|stem1POS|stem1-STEM1SFX_stem2POS|stem2-STEM2SFX
        word1:
            seg = stem1 gloss = ???         pos = stem1POS
            seg = ???   gloss = STEM1SFX    pos = sfx
        word2:
            seg = stem2 gloss = ???         pos = stem2POS
            seg = ???   gloss = STEM2SFX    pos = sfx
        """
        wwords = utterance.split(' ')
        mwords = morph_tier.split(' ')
        wwords_count = len(wwords)
        mwords_count = len(mwords)

        i = 0
        while i < wwords_count and i < mwords_count:
            # check for double POS tag
            match = re.search(r'\S+?\|(\S+\|.*)', mwords[i])
            if match:
                # discard POS tag of whole complex
                mword = match.group(1)
                # remove old word
                del mwords[i]
                mwords_count -= 1
                # add new words
                for j, w in enumerate(re.split(r'[+_]', mword)):
                    mwords.insert(i+j, w)
                    mwords_count += 1

                # check if utterance word is also joined
                if '_' in wwords[i] or '+' in wwords[i]:
                    # same procedure
                    wword = wwords[i]
                    del wwords[i]
                    wwords_count -= 1
                    for j, w in enumerate(re.split(r'[+_]', wword)):
                        wwords.insert(i + j, w)
                        wwords_count += 1
            i += 1

        return ' '.join(wwords), ' '.join(mwords)

    @classmethod
    def utterance_cross_clean(
            cls, raw_utt, actual_utt, target_utt,
            seg_tier, gloss_tier, pos_tier):
        """Cross clean between word and segment utterances."""
        # which morphology tier does not matter, they are all the same
        mor_tier = seg_tier
        actual_utt, mor_tier = cls.single_morph_word(actual_utt, mor_tier)
        actual_utt, mor_tier = cls.separate_morph_word(actual_utt, mor_tier)
        target_utt, mor_tier = cls.single_morph_word(target_utt, mor_tier)
        target_utt, mor_tier = cls.separate_morph_word(target_utt, mor_tier)

        return actual_utt, target_utt, mor_tier, mor_tier, mor_tier

    # ---------- word cleaning ----------

    @staticmethod
    def replace_plus(unit):
        """Replace plus by an underscore.

        Args:
            unit (str): utterance word or segment
        """
        return unit.replace('+', '_')

    @classmethod
    def clean_word(cls, word):
        word = super().clean_word(word)
        return cls.replace_plus(word)

    # ---------- utterance cleaning ----------

    @staticmethod
    def unify_untranscribed(utterance):
        """Unify untranscribed material as ???.

        Same as super method. Additionally, also unifies more than three `y`s,
        `ww` and `x`.
        """
        untranscribed_regex = re.compile(r'\b((?<!\[)x+|y{3,}|w{2,})\b')
        return untranscribed_regex.sub(r'???', utterance)

    # ---------- morpheme cleaning ----------

    # ---------- segment cleaning ----------

    @classmethod
    def clean_segment(cls, segment):
        return cls.replace_plus(segment)

    # ---------- morpheme cleaning ----------

    @classmethod
    def clean_gloss(cls, gloss):
        return TurkishGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return TurkishPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return TurkishPOSMapper.map(pos_ud, ud=True)
