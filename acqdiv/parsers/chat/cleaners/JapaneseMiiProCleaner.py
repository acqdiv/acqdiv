import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner


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
        return cls.remove_redundant_whitespaces(morph_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        morph_tier = cls.remove_terminator(morph_tier)
        return cls.remove_non_words(morph_tier)

    # ---------- cross cleaning ----------

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
            return date[:4] + '-' + date[4:6] + date[6:8]

        return date

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
