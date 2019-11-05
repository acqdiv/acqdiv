import re

from acqdiv.parsers.chat.readers.reader import CHATReader


class NungonReader(CHATReader):

    # ---------- morphology tier ----------

    def get_seg_tier(self):
        """Get the segment tier.

        The name of the segment tier can be either 'xgls' or 'gls'. The former
        is more common.
        """
        for seg_tier_name in ['xgls', 'gls']:
            if seg_tier_name in self.record.dependent_tiers:
                return self.record.dependent_tiers[seg_tier_name]
        return ''

    def get_gloss_tier(self):
        return self.record.dependent_tiers.get('xcod', '')

    def get_pos_tier(self):
        return self.record.dependent_tiers.get('xcod', '')

    # ---------- morpheme words ----------

    @classmethod
    def get_morpheme_words(cls, morph_tier):
        """Get the morpheme words of the morphology tier.

        Morpheme words are normally separated by whitespaces. Clitics are
        separated by '=' and are split off in parsing as they correspond
        to independent words in the utterance.
        """
        if morph_tier:
            return re.split(r'\s+|=', morph_tier)
        else:
            return []

    # ---------- morphemes ----------

    @classmethod
    def get_segments(cls, seg_word):
        """Segments are separated by dashes."""
        if seg_word:
            return seg_word.split('-')
        else:
            return []

    @staticmethod
    def iter_gloss_pos(gloss_pos_word):
        """Iter glosses and POS tags of a word.

        Morphemes are separated by dashes ('-'). Stems have a POS tag which is
        prefixed to the gloss by a caret ('^'). Prefixes and suffixes have only
        explicit glosses. They receive the POS tag 'pfx' and 'sfx',
        respectively. Some words do not have a stem marker in which case all
        morphemes get only glosses but no POS tags assigned.

        Yields:
            tuple: (gloss, POS tag)
        """
        morphemes = gloss_pos_word.split('-')

        # check if there is a stem marker
        if '^' not in gloss_pos_word:
            for gloss in morphemes:
                yield gloss, ''
        else:
            stem_passed = False
            for morpheme in morphemes:
                # check if it is the stem
                if '^' in morpheme:
                    # match POS up to the last ^ (in case there are several ^)
                    match = re.search(r'(.*)\^(.*)', morpheme)
                    gloss = match.group(2)
                    pos = match.group(1)
                    stem_passed = True
                else:
                    gloss = morpheme
                    if stem_passed:
                        pos = 'sfx'
                    else:
                        pos = 'pfx'

                yield gloss, pos

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for gloss, _ in cls.iter_gloss_pos(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, pos in cls.iter_gloss_pos(pos_word)]

    @classmethod
    def get_morpheme_language(cls, seg, gloss, pos):
        """Get the morpheme language.

        The morpheme language is coded in the POS tag. If it starts with 'eng',
        the morpheme is English, if it starts with 'tp', the morpheme is Tok
        Pisin.
        """
        if pos.startswith('eng'):
            return 'English'
        elif pos.startswith('tp'):
            return 'Tok Pisin'
        else:
            return 'Nungon'
