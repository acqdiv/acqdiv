from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner


class ArabicKernCleaner(CHATCleaner):

    @classmethod
    def clean_speaker_metadata(
            cls, session_filename, label, name, role,
            age, gender, language, birth_date, target_child):

        birth_date = cls.correct_birthdate(birth_date, name)

        return label, name, role, age, gender, language, birth_date

    @staticmethod
    def correct_birthdate(birth_date, name):
        if birth_date == '2002-02-03' and name == 'Iyed':
            return '2002-01-30'

        return birth_date
