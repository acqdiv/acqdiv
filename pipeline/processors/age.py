from datetime import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
import re

class TimeDataError(Exception):
    """
    Base class for all exceptions in acqdiv.age.

    TimeDataError represents an exception occurring because of invalid
    time data. It is not used directly, but instead subclassed to represent
    the different kinds of time data processed in this module.
    """
    def __init__(self, bad_data, trigger=None):
        self.bad_data = bad_data
        self.trigger = trigger
        if bad_data is None:
            self.etype = "null"
        else:
            self.etype = "other"
        self.expected = "string"
        self.data_name = "time data"
        self.bad_data_repr = type(self.bad_data)

    def __repr__(self):
        return "TimeDataError({}, {})".format(
                self.bad_data, self.trigger)

    def __str__(self):
        if self.etype == "null":
            rstring = "empty {}, expected {}".format(
                    self.data_name, self.expected)
        else:
            rstring = "{} is {}, expected {}".format(
                    self.data_name, self.bad_data_repr, self.expected)
        return rstring

class BirthdateError(TimeDataError):
    """
    Subclass of TimeDataError representing a missing or invalid birth date.
    """

    def __init__(self, bad_data, trigger=None):
        super().__init__(bad_data, trigger)
        self.data_name = "birthdate"
        self.expected = "string in format YYYY-mm-dd"
        if isinstance(self.bad_data, str):
            self.bad_data_repr == self.bad_data
        else:
            self.bad_data_repr == type(self.bad_data)

    def __repr__(self):
        return "BirthdateError({}, {})".format(
                self.bad_data, self.trigger)

class SessionDateError(TimeDataError):
    """
    Subclass of TimeDataError representing a missing or invalid recording date.
    """

    def __init__(self, bad_data, trigger=None):
        super().__init__(bad_data, trigger)
        self.data_name = "session recording date"
        self.expected = "string in format YYYY-mm-dd"
        if isinstance(self.bad_data, str):
            self.bad_data_repr == self.bad_data
        else:
            self.bad_data_repr == type(self.bad_data)

    def __repr__(self):
        return "SessionDateError({}, {})".format(
                self.bad_data, self.trigger)

def numerize_date(date):
    """Converts dates with month names to dates with month digits.

    This function takes a string and replaces month abbreviation of the form
    'JAN', 'FEB', etc. with two-digit numbers. Also, to work around a problem
    with years in some of our corpora, it removes sequences of a slash and two
    digits.

    Args:
        date: A string representing a date.

    Returns:
        A string with month abbreviations replaced by digits.

    Examples:
        >>> numerize_date("12-JAN-1994")
        '12-01-1994'
    """
    date = str(date).replace('JAN', '01').replace('FEB', '02').replace('MAR', '03').replace('APR', '04').replace('MAY','05').replace('JUN','06').replace('JUL','07').replace('AUG','08').replace('SEP','09').replace('OCT','10').replace('NOV','11').replace('DEC','12').replace('"','')
    date = re.sub('/\d{2}', '', date)
    return date

def format_imdi_age(birthdate, sessiondate):
    """Function to calculate the age of speakers in IMDI corpora.

    This function attempts to calculate the age of a speaker from their
    birth date and the date the session was recorded. The dates must
    be in the format YYYY(-MM-DD).

    Args:
        birthdate: Birth date of the the speaker.
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
            raise BirthdateError(birthdate, bde)

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
                raise SessionDateError(sessiondate, sde)

    diff = relativedelta(d2, d1)
    diff_days = d2 - d1
    if acc_flag_bd != 1 and acc_flag_sd != 1:
        if acc_flag_sd != 2:
            age_cform = "{0};{1}.{2}".format(diff.years, diff.months, diff.days)
        else:
            age_cform = "{0};{1}.0".format(diff.years, diff.months)
    else: 
        age_cform = "{0};0.0".format(diff.years)

    age_days = int(diff_days.days)
    return([age_cform if age_cform != "0;0.0" else None, age_days if age_days != 0 else None])


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
        return (new_age, days)
    else:
        years = age.split('/')[0]
        clean_years = years + ";0.0"
        days = int(years) * 365
        return (clean_years, days)


def format_xml_age(age_str):
    """Reformats ages in XML corpora.

    Ages in the XML corpora are usually given in the format "P0Y0M0D",
    where preceding the Y is the number of years, preceding the M is the number
    of months, and preceding the D is the number of days.

    This function transforms these ages into our target format of "YY;MM.DD".
    Sometimes, we only get P0Y0M. In this case, we return "YY;MM.0".

    Args:
        age_str: A string representing an age in the format P0Y0M0D.

    Returns:
        The age string in the format YY;MM.DD, or None if an invalid string
        is passed in.
    """
    age_str = age_str.split('/')[0]
    age = re.match(r'P(\d*)Y(\d*)?M?(\d*)?D?', age_str)
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
        return("{0};{1}.{2}".format(years, months, days))
    else:
        return None

def calculate_xml_days(age_str):
    """Calculates the age in days of a speaker from a formatted age string.

    This function takes a string representing an age in our target format of
    YY;MM.DD and calculates the number of days represented by it.

    Args:
        age_str: A string representing an age in the format YY;MM.DD

    Returns:
        An integer representing the age in days of the speaker.
    """
    age = re.match("(\d*);(\d*).(\d*)", age_str)
    years = int(age.group(1))
    months = int(age.group(2))
    days = int(age.group(3))
    out = years * 365 + months * 30 + days
    return out

def unify_timestamps(timestamp_str):
    """Unifies the format of timestamps across corpora.

    Takes a string representing the time position in the session recording
    in the format HH:MM:SS.mmmm and returns the equivalent in seconds and 
    milliseconds.

    Args:
        timestamp_str: The timestamp of an utterance.

    Returns:
        The timestamp in seconds and milliseconds.
    """
    if timestamp_str is None:
        return None
    times = re.match(r'(\d+):(\d+):(\d+)\.?(\d+)?', timestamp_str)
    if times:
        fields = times.lastindex
        if fields == 4:
            seconds = int(times.group(1)) * 3600 + int(times.group(2)) * 60 + int(times.group(3))
            msecs = times.group(4)
            return("{0}.{1}".format(seconds, msecs))
        elif fields == 3:
            times = re.match(r'(\d+):(\d+):(\d+)', timestamp_str)
            if times:
                seconds = int(times.group(1)) * 3600 + int(times.group(2)) * 60 + int(times.group(3))
                return("{0}.000".format(seconds))
        else:
            return None
    else:
        return timestamp_str
