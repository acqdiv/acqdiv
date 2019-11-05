import re

from acqdiv.parsers.chat.readers.reader import CHATReader


class EnglishManchester1Reader(CHATReader):

    # TODO: move all corrections to cleaner

    @staticmethod
    def correct_speaker_name(name, label, role, target_child_name, pid):
        """Correct speaker name.

        Corrections:
        - if target child = 'Carl' and speaker_label = 'FAT', set name to 'Ian'
        - if label = RAC, set name to Rachel
        - if name = 'Mother', change to [speaker_role of target_child_name]
        - if name = 'Father', change to [speaker_role of target_child_name]
        - if name = 'Grandfather', change to
            [speaker_role of target_child_name]
        - if name missing and label != INV
            set name to [speaker_role of target_child_name]
        - if name == 'CHI' (and PID == '11312/c-00019860-1'):
            set name to 'Liz'
        """
        # order is important!
        if target_child_name == 'Carl' and label == 'FAT':
            return 'Ian'
        elif name in {'Mother', 'Father', 'Grandfather'}:
            return role + ' of ' + target_child_name
        elif name == 'CHI' and pid == '11312/c-00019860-1':
            return 'Liz'
        elif name:
            return name
        else:
            if label == 'RAC':
                return 'Rachel'
            elif label != 'INV':
                return role + ' of ' + target_child_name
            else:
                return name

    def get_speaker_name(self):
        """Get speaker name."""
        name = super().get_speaker_name()
        label = self.get_speaker_label()
        role = self.get_speaker_role()
        target_child_name = self.get_target_child()[1]
        pid = self.chat.pid

        return self.correct_speaker_name(
            name, label, role, target_child_name, pid)

    @staticmethod
    def correct_speaker_label(label):
        """Correct speaker label.

        Corrections:
        - if label = DAD, change to 'FAT'
        """
        if label == 'DAD':
            return 'FAT'
        else:
            return label

    def get_speaker_label(self):
        label = super().get_speaker_label()
        return self.correct_speaker_label(label)

    def get_record_speaker_label(self):
        label = super().get_record_speaker_label()
        return self.correct_speaker_label(label)

    def get_translation(self):
        return self.get_utterance()

    @staticmethod
    def get_word_language(word):
        if word.endswith('@s:fra'):
            return 'French'
        elif word.endswith('@s:ita'):
            return 'Italian'
        else:
            return 'English'

    @staticmethod
    def iter_morphemes(morph_word):
        """Iter morphemes of a word.

        A word consists of word groups in the case of
            - compounds (marker: +)
            - clitics (marker: ~)

        A word group has the following structure:
        prefix#POS|stem&fusionalsuffix-suffix=gloss

        prefix: segment, no gloss (-> assign segment), no POS (-> assign 'pfx')
        stem: segment, gloss (either from '='-part or segment), POS
        suffix: no segment, gloss, no POS (-> assign 'sfx')

        For every component of the compound '=' is prepended to the part (e.g.
        'n|+n|apple+n|tree' -> '=apple', '=tree'). The POS tag of the whole
        compound is removed.

        Returns:
            tuple: (segment, gloss, pos).
        """
        morpheme_regex = re.compile(r'[^#]+#'
                                    r'|[^\-]+'
                                    r'|[\-][^\-]+')

        # split into word groups (in case of compound, clitic) (if applicable)
        word_groups = re.split(r'[+~]', morph_word)

        # check if word is a compound
        if word_groups[0].endswith('|'):
            # remove POS tag of the whole compound
            del word_groups[0]
            is_compound = True
        else:
            is_compound = False

        for word_group in word_groups:

            # get stem gloss and remove it from morpheme word
            match = re.search(r'(.+)=(\S+)$', word_group)
            if match:
                word_group = match.group(1)
                stem_gloss = match.group(2)
            else:
                stem_gloss = ''

            # iter morphemes
            for match in morpheme_regex.finditer(word_group):
                morpheme = match.group()

                # prefix
                if morpheme.endswith('#'):
                    pfx = morpheme.rstrip('#')
                    segment = pfx
                    gloss = segment
                    pos = 'pfx'
                # sfx
                elif morpheme.startswith('-'):
                    sfx = morpheme.lstrip('-')
                    segment = ''
                    gloss = sfx
                    pos = 'sfx'
                # stem
                else:
                    pos, segment = morpheme.split('|')
                    # take gloss from '='-part, otherwise the segment
                    if stem_gloss:
                        gloss = stem_gloss
                    else:
                        gloss = segment

                    # if it is a compound part
                    if is_compound:
                        # prepend '=' to segment
                        segment = '=' + segment

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

    @staticmethod
    def get_morpheme_language(seg, gloss, pos):
        if pos == 'L2':
            return 'FOREIGN'
        else:
            return 'English'
