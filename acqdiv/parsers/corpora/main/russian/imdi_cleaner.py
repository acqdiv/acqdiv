from acqdiv.parsers.toolbox.cleaners.imdi_cleaner import IMDICleaner


class RussianIMDICleaner(IMDICleaner):

    @classmethod
    def clean_gender(cls, gender):
        gender = super().clean_gender(gender)
        return gender.title()
