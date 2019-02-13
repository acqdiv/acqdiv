import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner


class JapaneseMiiProCleaner(CHATCleaner):

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
    def clean_speaker_metadata(
            cls, session_filename, speaker_label, name, role,
            age, gender, language, birth_date, target_child):
        role = cls.correct_role(speaker_label, role, target_child)
        name = cls.correct_name(session_filename, speaker_label, name)

        return speaker_label, name, role, age, gender, language, birth_date

    @staticmethod
    def correct_role(speaker_label, role, target_child):
        if role == 'Child' and speaker_label == target_child[0]:
            return 'Target_Child'

        return role

    @staticmethod
    def correct_name(session_filename, speaker_label, name):

        if session_filename.startswith('als'):
            if name == 'Asatokun':
                return 'Asato'
            elif speaker_label == 'MOT':
                return 'Mother_of_Arika_and_Asato'
            elif speaker_label == 'ALS':
                return 'Asato'

        elif session_filename.startswith('aprm'):
            if name == 'Arichan':
                return 'Arika'
            elif name == 'Akko':
                return 'Mother_of_Arika_and_Asato'
            elif name == 'Asatokun':
                return 'Asato'

        elif session_filename.startswith('njd'):
            if name == 'Jurichan':
                return 'Juri'
            elif name == 'Natchan':
                return 'Nanami'
            elif name == 'Okaasan':
                return 'Mother_of_Nanami'
            elif name == 'Arikachan':
                return 'Arika'
            elif speaker_label == 'MOT':
                return 'Mother_of_Nanami'
            elif speaker_label == 'NJD':
                return 'Nanami'

        elif session_filename.startswith('tom'):
            if name == 'Honokachan':
                return 'Honoka'
            elif speaker_label == 'MOT':
                return 'Mother_of_Tomito'

        return name
