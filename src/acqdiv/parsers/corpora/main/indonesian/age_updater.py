import re
from acqdiv.util.age import get_age_from_birth_date_session_date, get_age_in_days


class IndonesianAgeUpdater:

    @classmethod
    def update(cls, speaker, recording_date):
        """Update `age` and `age_in_days` for speaker.

        Args:
            speaker (acqdiv.model.speaker.Speaker): The speaker.
            recording_date (str): The recording date.
        """
        ages = get_age_from_birth_date_session_date(speaker.birth_date,
                                                    recording_date)

        speaker.age = ages[0]
        speaker.age_in_days = ages[1]

        if not speaker.age:
            speaker.age = cls.clean(speaker.age_raw)

        if not speaker.age_in_days:
            speaker.age_in_days = get_age_in_days(speaker.age)

    @staticmethod
    def clean(age_raw):
        """Clean the age in Indonesian.

        Ages are given in the format "P0Y0M0D", where preceding the Y is 
        the number of years, preceding the M is the number of months, 
        and preceding the D is the number of days.

        This function transforms these ages into our target format "YY;MM.DD".
        Sometimes, we only get P0Y0M. In this case, we return "YY;MM.0".

        Args:
            age_raw: The age in the format P0Y0M0D.

        Returns:
            str: The age in the format YY;MM.DD.
        """
        age_raw = age_raw.split('/')[0]
        age = re.match(r'P(\d*)Y(\d*)?M?(\d*)?D?', age_raw)
        if age:
            if age.group(3) != '':
                days = age.group(3)
            else:
                days = "0"
            if age.group(2) != '':
                months = age.group(2)
            else:
                months = "0"
            years = age.group(1)
            return "{0};{1}.{2}".format(years, months, days)
        else:
            return ''
