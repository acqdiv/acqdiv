import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_age_from_birth_date_session_date(birthdate, sessiondate):
    """Calculate the age from the birth date and the session date.

    This function attempts to calculate the age of a speaker from their
    birth date and the date the session was recorded. The dates must
    be in the format YYYY(-MM-DD).

    Args:
        birthdate (str): Birth date of the the speaker.
        sessiondate: Date the session was recorded.

    Returns:
        An age in the form YY;MM.DD

    Raises:
        BirthdateError: the speaker's birth date is None or invalid
        SessionDateError: the session recording date is None or invalid
    """
    acc_flag_bd = 0
    acc_flag_sd = 0
    try:
        d1 = datetime.strptime(birthdate, "%Y-%m-%d")
    except:
        try:
            d1 = datetime.strptime(birthdate, "%Y")
            acc_flag_bd = 1
        except Exception as bde:
            return ['', '']

    try:
        d2 = datetime.strptime(sessiondate, "%Y-%m-%d")
    except:
        try:
            d2 = datetime.strptime(sessiondate, "%Y")
            acc_flag_sd = 1
        except:
            try:
                d2 = datetime.strptime(sessiondate, "%Y-%m")
                acc_flag_sd = 2
            except Exception as sde:
                return ['', '']

    diff = relativedelta(d2, d1)
    diff_days = d2 - d1
    if acc_flag_bd != 1 and acc_flag_sd != 1:
        if acc_flag_sd != 2:
            age_cform = "{0};{1}.{2}".format(diff.years, diff.months,
                                             diff.days)
        else:
            age_cform = "{0};{1}.0".format(diff.years, diff.months)
    else:
        age_cform = "{0};0.0".format(diff.years)

    age_days = int(diff_days.days)
    return ([age_cform if age_cform != "0;0.0" else None,
             age_days if age_days != 0 else None])


def get_age_in_days(age):
    """Convert the age to days.

    This function takes a string representing an age in our target format
    of YY;MM.DD and calculates the number of days represented by it.

    Args:
        age (str): The age in the format YY;MM.DD.

    Returns:
        int: The age in days.
    """
    age = re.match(r"(\d*);(\d*).(\d*)", age)
    if age:
        years = int(age.group(1))
        months = int(age.group(2))
        days = int(age.group(3))
        out = years * 365 + months * 30 + days
        return out

    return ''
