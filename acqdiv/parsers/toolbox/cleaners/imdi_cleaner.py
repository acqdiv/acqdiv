

class IMDICleaner:

    null_values = {'Unknown', 'Unspecified', 'None', 'Unidentified'}

    @classmethod
    def unify_unknowns(cls, value):
        if value in cls.null_values:
            return ''
        else:
            return value

    @classmethod
    def clean_date(cls, date):
        return cls.unify_unknowns(date)

    @classmethod
    def clean_name(cls, name):
        return cls.unify_unknowns(name)

    @classmethod
    def clean_gender(cls, gender):
        return cls.unify_unknowns(gender)

    @classmethod
    def clean_label(cls, label):
        return cls.unify_unknowns(label)
