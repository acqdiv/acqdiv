import re

from acqdiv.parsers.chat.readers.reader import CHATReader

from acqdiv.parsers.corpora.main.\
    japanese_miipro.gloss2segment_mapper \
    import JapaneseMiiProGloss2SegmentMapper as Mp


class JapaneseMiiProReader(CHATReader):

    @classmethod
    def _is_target_child(cls, pos, role):
        if role == 'Target_Child':
            return True

        if role == 'Child' and pos == 0:
            return True

        return False

    def get_target_child(self):
        for pos, (code, p) in enumerate(self.chat.participants.items()):
            if self._is_target_child(pos, p.role):
                return code, p.name

        return '', ''

    def get_morph_tier(self):
        if self.record.dependent_tiers.get('xtrn', ''):
            return self.record.dependent_tiers.get('xtrn', '')
        else:
            return self.record.dependent_tiers.get('xmor', '')

    @staticmethod
    def get_word_language(word):
        if word.endswith('@s:eng'):
            return 'English'
        else:
            return 'Japanese'

    @staticmethod
    def iter_morphemes(morph_word):
        """Iter morphemes of a word.

        A word consists of word groups in the case of compounds (marker: +).

        A word group has the following structure:
        prefix#POS|stem&fusionalsuffix-suffix=gloss

        prefix: segment, no gloss, no POS (-> assign 'pfx')
        stem: segment, gloss, POS
        suffix: no segment, with gloss, without POS (-> assign 'sfx')

        For every component of the compound '=' is prepended to the part (e.g.
        'n|+n|apple+n|tree' -> '=apple', '=tree'). Both parts receive the same
        gloss. The POS tag of the whole compound is removed. There may be
        prefixes attached to the whole compound. There are no clitics.

        Suffixes with a colon are specially treated: If the part after the
        colon is not 'contr' (contraction), it denotes the segment of the
        suffix.

        Returns:
            tuple: (segment, gloss, pos).
        """
        morpheme_regex = re.compile(r'[^#]+#'
                                    r'|[^\-]+'
                                    r'|[\-][^\-]+')

        # get stem gloss and remove it from morpheme word
        match = re.search(r'(.+)=(\S+)$', morph_word)
        if match:
            morph_word = match.group(1)
            stem_gloss = match.group(2)
        else:
            stem_gloss = ''

        # split into word groups (i.e. into compound parts) (if applicable)
        word_groups = morph_word.split('+')

        # check if word is a compound
        if len(word_groups) > 1:
            # pop prefixes & the POS tag of the whole compound
            pfxs_cmppos = word_groups.pop(0)

            # iter prefixes preceding compound
            for pfx_match in re.finditer(r'[^#]+(?=#)', pfxs_cmppos):
                yield pfx_match.group(), '', 'pfx'

        for word_group in word_groups:

            # iter morphemes
            for match in morpheme_regex.finditer(word_group):
                morpheme = match.group()

                # prefix
                if morpheme.endswith('#'):
                    segment = morpheme.rstrip('#')
                    gloss = ''
                    pos = 'pfx'
                # sfx
                elif morpheme.startswith('-'):
                    sfx = morpheme.lstrip('-')
                    pos = 'sfx'
                    match = re.search(r'([^:]+)(:(.*))?', sfx)
                    # check for colon case
                    if match.group(2) and match.group(3) != 'contr':
                        segment = match.group(3)
                        gloss = match.group(1)
                    else:
                        segment = ''
                        gloss = sfx
                # stem
                else:
                    pos, segment = morpheme.split('|')
                    # if it is a compound part
                    if len(word_groups) > 1:
                        # prepend '=' to segment
                        segment = '=' + segment
                    gloss = stem_gloss

                if Mp.map(gloss):
                    segment = Mp.map(gloss)

                yield segment, gloss, pos

    @classmethod
    def get_segments(cls, seg_word):
        return [seg for seg, _, _ in cls.iter_morphemes(seg_word)]

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, gloss, _ in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, _, pos in cls.iter_morphemes(pos_word)]
