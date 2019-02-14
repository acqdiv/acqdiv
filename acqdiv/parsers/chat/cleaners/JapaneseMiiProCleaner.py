import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner


class JapaneseMiiProCleaner(CHATCleaner):

    @staticmethod
    def correct_speaker_label(session_filename, speaker_label):
        sessions_filenames = {
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

        if session_filename in sessions_filenames and speaker_label == 'CHI':
            return 'ALS'

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

        tc_label, _ = target_child
        tc_label = cls.correct_speaker_label(session_filename, tc_label)
        label = cls.correct_speaker_label(session_filename, label)
        role = cls.correct_role(label, role, tc_label)
        name = cls.correct_name(session_filename, label, name)

        return label, name, role, age, gender, language, birth_date

    @staticmethod
    def correct_role(label, role, tc_label):
        if role == 'Child' and label == tc_label:
            return 'Target_Child'

        return role

    @staticmethod
    def correct_name(session_filename, label, name):

        if session_filename.startswith('als'):
            if name == 'Asatokun':
                return 'Asato'
            elif name == 'Arichan':
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
            if name == 'Jurichan':
                return 'Juri'
            elif name == 'Natchan':
                return 'Nanami'
            elif name == 'Fuyumichan':
                return 'Fuyumi'
            elif label == 'MOT':
                return 'Mother_of_Nanami'
            elif name == 'Arikachan':
                return 'Arika'
            elif name == 'Kantakun':
                return 'Kanta'
            elif label == 'MOT':
                return 'Mother_of_Nanami'
            elif label == 'MTO':
                return 'Mother_of_Tomito'
            elif label == 'NJD':
                return 'Nanami'

        elif session_filename.startswith('tom'):
            if name == 'Honokachan':
                return 'Honoka'
            elif label == 'MOT':
                return 'Mother_of_Tomito'

        return name
