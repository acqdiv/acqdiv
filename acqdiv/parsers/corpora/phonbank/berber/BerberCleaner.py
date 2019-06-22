from acqdiv.parsers.chat.cleaners.BaseCHATCleaner import BaseCHATCleaner


class BerberCleaner(BaseCHATCleaner):

    @classmethod
    def clean_speaker_metadata(
            cls, session_filename, label, name, role,
            age, gender, language, birth_date, target_child):

        name = cls.get_name(session_filename)

        return label, name, role, age, gender, language, birth_date

    @classmethod
    def get_name(cls, session_filename):
        return session_filename.split('_')[0]
