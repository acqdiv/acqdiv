from acqdiv.parsers.chat.cleaners.BaseCHATCleaner import BaseCHATCleaner


class PolishCleaner(BaseCHATCleaner):

    @classmethod
    def clean_speaker_metadata(
            cls, session_filename, label, name, role,
            age, gender, language, birth_date, target_child):

        _, tc_name = target_child
        name = cls.correct_name(name, tc_name)
        #birth_date = cls.correct_birthdate(birth_date)

        return label, name, role, age, gender, language, birth_date

    @staticmethod
    def correct_birthdate(birth_date):
        """Null dummy birth dates."""
        if birth_date == '1954-01-01':
            return ''

        return birth_date

    @staticmethod
    def correct_name(name, tc_name):
        names = {
            'Mother',
            'Father',
            'Aunt',
            'Grandmother',
            'Grandfather',
            'Family_Friend'
        }
        if name in names:
            return name + '_of_' + tc_name

        return name
