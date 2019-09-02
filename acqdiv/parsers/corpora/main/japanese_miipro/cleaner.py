import re

from acqdiv.parsers.chat.cleaners.cleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.utterance_cleaner \
    import CHATUtteranceCleaner
from acqdiv.parsers.corpora.main.japanese_miipro.gloss_mapper \
    import JapaneseMiiProGlossMapper as GMp
from acqdiv.parsers.corpora.main.japanese_miipro.pos_mapper \
    import JapaneseMiiProPOSMapper as PMp


class JapaneseMiiProCleaner(CHATCleaner):

    @staticmethod
    def correct_speaker_label(session_filename, speaker_label):
        """Replace `CHI` label of target child."""
        if speaker_label == 'CHI':
            if session_filename.startswith('Asato'):
                return 'ALS'
            elif session_filename.startswith('Arika'):
                return 'APR'
            elif session_filename.startswith('Nanami'):
                return 'NJD'
            elif session_filename.startswith('Tomito'):
                return 'TOM'

        return speaker_label

    @classmethod
    def clean_record_speaker_label(cls, session_filename, speaker_label):
        speaker_label = cls.correct_speaker_label(
            session_filename, speaker_label)
        return speaker_label

    # ---------- morphology tier cleaning ----------

    @classmethod
    def remove_non_words(cls, morph_tier):
        """Remove all non-words from the morphology tier.

        Non-words have the POS tag 'tag'.
        """
        non_words_regex = re.compile(r'tag\|\S+')
        morph_tier = non_words_regex.sub('', morph_tier)
        return CHATUtteranceCleaner.remove_redundant_whitespaces(morph_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        morph_tier = CHATUtteranceCleaner.remove_terminator(morph_tier)
        return cls.remove_non_words(morph_tier)

    # ---------- speaker metadata cleaning ----------

    @classmethod
    def clean_speaker_metadata(
            cls, session_filename, label, name, role,
            age, gender, language, birth_date, target_child):
        """Correct label, role and name of speaker."""

        tc_label, _ = target_child
        tc_label = cls.correct_speaker_label(session_filename, tc_label)
        label = cls.correct_speaker_label(session_filename, label)
        role = cls.correct_role(label, role, tc_label)
        name = cls.correct_name(session_filename, label, name)

        return label, name, role, age, gender, language, birth_date

    @staticmethod
    def correct_role(label, role, tc_label):
        """Correct role of target child.

        Returns:
            str: The corrected role.
        """
        if role == 'Child' and label == tc_label:
            return 'Target_Child'

        return role

    @staticmethod
    def correct_name(session_filename, label, name):
        """Correct name of speaker.

        Returns:
            str: The corrected name.
        """
        if session_filename.startswith('Asato'):
            if name == 'Asatokun':
                return 'Asato'
            elif label == 'APR':
                return 'Arika'
            elif label == 'MOT':
                return 'Mother_of_Arika_and_Asato'
            elif label == 'ALS':
                return 'Asato'

        elif session_filename.startswith('Arika'):
            if name == 'Arichan':
                return 'Arika'
            elif label == 'MOT':
                return 'Mother_of_Arika_and_Asato'
            elif name == 'Asatokun':
                return 'Asato'
            elif label == 'APR':
                return 'Arika'
            elif label == 'BAA':
                return 'Obaachan'

        elif session_filename.startswith('Nanami'):
            if name == 'Natchan':
                return 'Nanami'
            elif name == 'Fuyumichan':
                return 'Fuyumi'
            elif label == 'MOT':
                return 'Mother_of_Nanami'
            elif name == 'Arikachan':
                return 'Arika'
            elif name == 'Arichan':
                return 'Arika'
            elif name == 'Kantakun':
                return 'Kanta'
            elif name == 'Totchan':
                return 'Tomito'
            elif label == 'MTO':
                return 'Mother_of_Tomito'
            elif label == 'NJD':
                return 'Nanami'
            elif label == 'TMO' and name == "Totchan's_Mother":
                name = 'Mother_of_Tomito'

        elif session_filename.startswith('Tomito'):
            if name == 'Honokachan':
                return 'Honoka'
            elif name == 'Tomitokun':
                return 'Tomito'
            elif name == 'Totchan':
                return 'Tomito'
            elif label == 'APR':
                return 'Arika'
            elif label == 'MOT':
                return 'Mother_of_Tomito'

        return name

    # ---------- utterance cross clean ----------

    @classmethod
    def utterance_cross_clean(
            cls, raw_utt, actual_utt, target_utt,
            seg_tier, gloss_tier, pos_tier):

        seg_tier = cls.add_repetitions(raw_utt, seg_tier)
        gloss_tier = cls.add_repetitions(raw_utt, gloss_tier)
        pos_tier = cls.add_repetitions(raw_utt, pos_tier)

        seg_tier = cls.add_retracings(raw_utt, actual_utt, seg_tier)
        gloss_tier = cls.add_retracings(raw_utt, actual_utt, gloss_tier)
        pos_tier = cls.add_retracings(raw_utt, actual_utt, pos_tier)

        return actual_utt, target_utt, seg_tier, gloss_tier, pos_tier

    @classmethod
    def add_repetitions(cls, raw_utt, morph_tier):
        """Add repetitions to morphology tier."""
        # check if there are any repetitions
        if '[x ' in raw_utt:

            # execute same cleaning steps except those for scoped symbols
            for cleaning_method in [
                    CHATUtteranceCleaner.remove_terminator,
                    CHATUtteranceCleaner.unify_untranscribed,
                    CHATUtteranceCleaner.remove_events,
                    CHATUtteranceCleaner.remove_omissions,
                    CHATUtteranceCleaner.remove_linkers,
                    CHATUtteranceCleaner.remove_separators,
                    CHATUtteranceCleaner.remove_ca,
                    CHATUtteranceCleaner.remove_pauses_between_words,
                    CHATUtteranceCleaner.remove_commas,
                    CHATUtteranceCleaner.null_event_utterances
                    ]:
                raw_utt = cleaning_method(raw_utt)

            # remove scoped symbols except for repetitions
            scope_regex = re.compile(r'\[[^x].*?\]')
            raw_utt = scope_regex.sub('', raw_utt)
            raw_utt = CHATUtteranceCleaner.remove_redundant_whitespaces(
                raw_utt)

            # get words from utterance and morphology tier
            utt_words = re.split(r'(?<!\[x) (?!\[x)', raw_utt)
            morph_words = morph_tier.split(' ')

            # check for misalignments
            if len(utt_words) == len(morph_words):

                morph_new = []
                group = []
                for uw, mw in zip(utt_words, morph_words):

                    morph_new.append(mw)
                    match = re.search(r'\[x (\d+)', uw)

                    if uw.startswith('<'):
                        group = [mw]
                    elif match:
                        reps = int(match.group(1))
                        if group:
                            group.append(mw)
                            morph_new += (reps-1)*group
                            group = []
                        else:
                            morph_new += (reps-1)*[mw]
                    elif group:
                        group.append(mw)

                return ' '.join(morph_new)

        return morph_tier

    @classmethod
    def add_retracings(cls, raw_utt, actual_utt, morph_tier):
        """Add retracings to morphology tiers.

        Uses a fuzzy matching approach as the retracings are not always used
        correctly in the corpus. For example, in some cases they are used for
        repetitions: < soo soo > [/] soo.

        Only considers retracings of up to 2 words.
        """
        # only perform steps if there are retracings
        if '[/]' in raw_utt and morph_tier:

            regex = re.compile(r'((\S+)( \2)+)|((\S+) (\S+)( \5 \6)+)')
            actual_utt = ' '.join(
                [cls.clean_word(word) for word in actual_utt.split(' ')])
            repeated_words = list(regex.finditer(actual_utt))

            morph_words = morph_tier.split(' ')
            new = []
            for i, mword in enumerate(morph_words):

                new.append(mword)

                if repeated_words:
                    repeated = repeated_words[0]

                    if repeated.group(1):
                        wword = repeated.group(2)
                        # first three letters have to match
                        if wword[:3] in mword:
                            n_reps = len(repeated.group(1).split(' ')) - 1
                            new += n_reps*[mword]
                            del repeated_words[0]

                    elif i > 0 and repeated.group(4):
                        wword1 = repeated.group(5)
                        wword2 = repeated.group(6)

                        if (wword1[:3] in morph_words[i-1]
                                and wword2[:3] in mword):
                            n_reps = len(
                                repeated.group(7).lstrip(' ').split(' ')) - 1
                            new += n_reps*(morph_words[i-1], mword)

            return ' '.join(new)

        return morph_tier

    # ---------- morpheme cleaning ----------

    @classmethod
    def clean_gloss(cls, gloss):
        return GMp.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return PMp.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return PMp.map(pos_ud, ud=True)
