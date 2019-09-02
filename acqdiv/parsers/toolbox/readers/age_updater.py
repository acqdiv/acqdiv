import re
from acqdiv.util.age import get_age_from_birth_date_session_date, get_age_in_days


class ToolboxAgeUpdater:

    age_pattern = re.compile(r".*;.*\..*")
    cleaned_age = re.compile(r'\d{1,2};\d{1,2}\.\d{1,2}')

    @classmethod
    def update(cls, speaker, recording_date):
        """Update age and age_in_days in speaker.

        First attempts to calculate ages from the speaker's birth date and
        the session's recording date. For speakers where this fails, looks for
        speakers that already have a properly formatted age, transfers this age
        from the age_raw column to the age column and calculates
        age_in_days from it.

        Finally, it looks for speakers that only have an age in years and
        does the same.

        Args:
            speaker (acqdiv.model.speaker.Speaker): The speaker.
            recording_date (str): The recording date.
        """

        if speaker.birth_date:
            ages = get_age_from_birth_date_session_date(speaker.birth_date,
                                                        recording_date)
            speaker.age = ages[0]
            speaker.age_in_days = ages[1]

        if not speaker.age and re.fullmatch(cls.age_pattern, speaker.age_raw):
            speaker.age = speaker.age_raw
            speaker.age_in_days = get_age_in_days(speaker.age)

        if ("None" not in speaker.age_raw
                and "Un" not in speaker.age_raw
                and not speaker.age):

            if not cls.cleaned_age.fullmatch(speaker.age_raw):
                try:
                    ages = cls.clean_incomplete_ages(speaker.age_raw)
                    speaker.age = ages[0]
                    speaker.age_in_days = ages[1]
                except ValueError:
                    pass

    @staticmethod
    def clean_incomplete_ages(age):
        """Cleanly formats an age given in terms of only years and months.

        Args:
            age: A string or integer representing the age in years and
                 optionally months of the speaker.

        Returns:
            A string in the form YY;MM.0 where MM is 0 if only years are given.
        """
        if ";" in age:
            parts = age.split(";")
            years = parts[0]
            months = parts[1]
            days = int(years) * 365 + int(months) * 30
            new_age = age + ".0"
            return new_age, days
        else:
            years = age.split('/')[0]
            clean_years = years + ";0.0"
            days = int(years) * 365
            return clean_years, days
