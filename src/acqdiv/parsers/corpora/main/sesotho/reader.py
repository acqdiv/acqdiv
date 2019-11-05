import re

from acqdiv.parsers.chat.readers.reader import CHATReader


class SesothoReader(CHATReader):
    """Class to implement Sesotho Reading methods.

    Normally the methods get_utterance(), get_actual_utterance() and
    get_target_utterance() extract the utterance from the mainline.
    In Sesotho there are many misalignments between the
    mainline-utterance and the morpheme-tiers. So instead the
    utterance (for all three methods) is created by joining morphemes to
    words and those to the utterance.
    """

    def __init__(self, session_file):
        super().__init__(session_file)
        self._passed_stem = False

    def _join_morph_to_utt(self):
        """Create the utterance by joining the morphemes to words.

        Morphemes are separated by hyphens. The hyphens are removed.
        """
        seg_tier = self.get_seg_tier()
        seg_words = seg_tier.split(' ')
        utt_words = []

        for w in seg_words:
            w = ''.join(w.split('-'))
            utt_words.append(w)

        return ' '.join(utt_words)

    def get_actual_utterance(self):
        """Get the actual utterance, created by joined morphemes."""
        return self._join_morph_to_utt()

    def get_target_utterance(self):
        """Get the target utterance, created by joined morphemes."""
        return self._join_morph_to_utt()

    def get_seg_tier(self):
        """Extract the segments tier and do cross-cleaning.

        Cross-cleaning has to be done from here for access to different
        tiers at the same time.
        """
        return self.record.dependent_tiers.get('gls', '')

    def get_gloss_tier(self):
        return self.record.dependent_tiers.get('xcod', '')

    def get_pos_tier(self):
        return self.record.dependent_tiers.get('xcod', '')

    def infer_pos(self, gloss, num_morphemes):
        """Infer the pos-tag for a gloss.

        Args:
            gloss: str, the gloss
            num_morphemes: int, the number of morphemes in the
                morpheme word
        Return:
            str, the pos-tag
        """
        if not gloss:
            return ''

        pos = ''
        # Check for prefixes and suffixes.
        if num_morphemes == 1 or (re.search(r'(v|id)\^|\(\d', gloss)
                                  or re.match(r'(aj$|nm$|ps\d+)', gloss)):
            self._passed_stem = True
            # Check for verbs: verbs have v^, one typo as s^.
            if re.search(r'[vs]\^', gloss):
                pos = 'v'

            # Check for nouns: nouns contains "(\d)" (default) or "ps/"
            elif re.search('\(\d+', gloss) or re.search('^ps/', gloss):
                pos = 'n'

            # Check for words with nominal concord.
            elif re.search(r'^(d|lr|obr|or|pn|ps|sr)\d+', gloss):
                pos_match = re.search('^(d|lr|obr|or|pn|ps|sr)\d+', gloss)
                pos = pos_match.group(1)

            # Check for particles: mostly without a precise gloss.
            elif re.search(
                    (r'^(aj|av|cd|cj|cm|ht|ij|loc|lr|ng|nm|obr|or|pr|q|sr'
                     r'|wh)$'),
                    gloss):
                pos = gloss

            # Check for free person markers.
            elif re.search(r'^sm\d+[sp]?$', gloss):
                pos = 'afx.detached'

            # Check for copulas.
            elif re.search(r'^cp|cp$', gloss):
                pos = 'cop'

            # Check for ideophones.
            elif re.search(r'id\^', gloss):
                pos = 'ideoph'

            # Check for meaningless and unclear words. Note that
            # "xxx" in the Sesotho coding tier is not the same as
            # CHAT "xxx" in the transcription tier - it does not
            # stand for words that could not be transcribed but for
            # words with unclear meaning.
            elif gloss == 'word' or gloss == 'xxx':
                pos = 'none'
            else:
                pos = '???'

        elif not self._passed_stem:
            pos = 'pfx'
        elif self._passed_stem:
            pos = 'sfx'

        return pos

    def iter_gloss_pos(self, gloss_word):
        """Iter glosses and poses of a gloss_word.

        This method only returns glosses and poses, but not segments,
        since segments are on a different tier. They are retrieved
        directly by get_segments().

        Glosses in a gloss_words (stems and affixes) are separated
        by hyphens.

        Args:
            gloss_word: str, the gloss of a word
        Returns:
            tuple: (gloss, pos).
        """
        if not gloss_word:
            yield ('', '')
        else:
            glosses = gloss_word.split('-')
            self._passed_stem = False
            for gloss in glosses:
                pos = self.infer_pos(gloss, len(glosses))
                yield (gloss, pos)

    @classmethod
    def get_segments(cls, seg_word):
        return seg_word.split('-')

    def get_glosses(self, gloss_word):
        return [gloss for gloss, _ in self.iter_gloss_pos(gloss_word)]

    def get_poses(self, pos_word):
        return [pos for _, pos in self.iter_gloss_pos(pos_word)]
