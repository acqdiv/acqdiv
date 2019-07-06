import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.CHATUtteranceCleaner \
    import CHATUtteranceCleaner


class JapaneseMiiProCleaner(CHATCleaner):

    @staticmethod
    def correct_speaker_label(session_filename, speaker_label):
        """Replace `CHI` label of target child."""
        als_files = {
            "als19990618.cha",
            "als19990706.cha",
            "als19990805.cha",
            "als19990907.cha",
            "als19991005.cha",
            "als19991207.cha",
            "als20000105.cha",
            "als20000201.cha",
            "als20000307.cha",
            "als20000404.cha",
            "als20000711.cha",
            "als20000905.cha",
            "als20001106.cha",
            "als20010108.cha",
            "als20010308.cha",
            "als20010512.cha",
            "als20010714.cha"
        }

        aprm_files = {
            "aprm19990515.cha",
            "aprm19990617.cha",
            "aprm19990714.cha",
            "aprm19990824.cha",
            "aprm19990915.cha",
            "aprm19991023.cha",
            "aprm19991128.cha",
            "aprm19991218.cha",
            "aprm20000123.cha",
            "aprm20000213.cha",
            "aprm20000301.cha",
            "aprm20000316.cha",
            "aprm20000417.cha",
            "aprm20000619.cha",
            "aprm20000716.cha",
            "aprm20000820.cha",
            "aprm20000904.cha",
            "aprm20001002.cha",
            "aprm20001030.cha",
            "aprm20001123.cha",
            "aprm20001210.cha",
            "aprm20010114.cha",
            "aprm20010128.cha",
            "aprm20010211.cha",
            "aprm20010223.cha",
            "aprm20010311.cha",
            "aprm20010517.cha",
            "aprm20010607.cha",
            "aprm20010702.cha"
        }

        njd_files = {
            "njd19970813.cha",
            "njd19970909.cha",
            "njd19970921.cha",
            "njd19971007.cha",
            "njd19971020.cha",
            "njd19971105.cha",
            "njd19971205.cha",
            "njd19971220.cha",
            "njd19980106.cha",
            "njd19980116.cha",
            "njd19980303.cha",
            "njd19980426.cha",
            "njd19980510.cha",
            "njd19980525.cha",
            "njd19980606.cha",
            "njd19980815.cha",
            "njd19980828.cha",
            "njd19980919.cha",
            "njd19981018.cha",
            "njd19990123.cha",
            "njd19990209.cha",
            "njd19990222.cha",
            "njd19990329.cha",
            "njd19990405.cha",
            "njd19990419.cha",
            "njd19990505.cha",
            "njd19990515.cha",
            "njd19990530.cha",
            "njd19990613.cha",
            "njd19990629.cha",
            "njd19990731.cha",
            "njd19990904.cha",
            "njd19991004.cha",
            "njd19991030.cha",
            "njd19991128.cha",
            "njd19991224.cha",
            "njd20000407.cha",
            "njd20000430.cha",
            "njd20000527.cha",
            "njd20000624.cha",
            "njd20000814.cha",
            "njd20000923.cha",
            "njd20001022.cha",
            "njd20001119.cha",
            "njd20001225.cha",
            "njd20010127.cha",
            "njd20010225.cha",
            "njd20010331.cha",
            "njd20010702.cha"
        }

        tom_files = {
            "tom19990528.cha",
            "tom19990629.cha",
            "tom19990804.cha",
            "tom19990903.cha",
            "tom19991004.cha",
            "tom19991102.cha",
            "tom19991130.cha",
            "tom20000105.cha",
            "tom20000202.cha",
            "tom20000306.cha",
            "tom20000407.cha",
            "tom20000605.cha",
            "tom20000808.cha",
            "tom20001002.cha",
            "tom20001215.cha",
            "tom20010307.cha",
            "tom20010518.cha",
            "tom20010724.cha"
        }

        if speaker_label == 'CHI':
            if session_filename in als_files:
                return 'ALS'
            elif session_filename in aprm_files:
                return 'APR'
            elif session_filename in njd_files:
                return 'NJD'
            elif session_filename in tom_files:
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

    # ---------- session metadata cleaning ----------

    @classmethod
    def clean_session_metadata(cls, session_filename, date, media_filename):
        """Correct the session date."""
        date = cls.correct_session_date(session_filename, date)
        return date, media_filename

    @staticmethod
    def correct_session_date(session_filename, date):
        match = re.search(r'\d{8}', session_filename)

        if match:
            date = match.group()
            return date[:4] + '-' + date[4:6] + '-' + date[6:8]

        return date

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
        if session_filename.startswith('als'):
            if name == 'Asatokun':
                return 'Asato'
            elif label == 'APR':
                return 'Arika'
            elif label == 'MOT':
                return 'Mother_of_Arika_and_Asato'
            elif label == 'ALS':
                return 'Asato'

        elif session_filename.startswith('aprm'):
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

        elif session_filename.startswith('njd'):
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

        elif session_filename.startswith('tom'):
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
