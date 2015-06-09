from datetime import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
import re

def numerize_date(date):
    date = str(date).replace('JAN', '01').replace('FEB', '02').replace('MAR', '03').replace('APR', '04').replace('MAY','05').replace('JUN','06').replace('JUL','07').replace('AUG','08').replace('SEP','09').replace('OCT','10').replace('NOV','11').replace('DEC','12').replace('"','')
    date = re.sub('/\d{2}', '', date)
    return date


def format_imdi_age(birthdate, sessiondate):
    acc_flag_bd = 0
    acc_flag_sd = 0
    try:
        d1 = datetime.strptime(birthdate, "%Y-%m-%d")
    except:
        d1 = datetime.strptime(birthdate, "%Y")
        acc_flag_bd = 1

    try:
        d2 = datetime.strptime(sessiondate, "%Y-%m-%d")
    except:
        try:
            d2 = datetime.strptime(sessiondate, "%Y")
            acc_flag_sd = 1
        except:
            d2 = datetime.strptime(sessiondate, "%Y-%m")
            acc_flag_sd = 2

    diff = relativedelta(d2, d1)
    diff_days = d2 - d1
    if acc_flag_bd != 1 and acc_flag_sd != 1:
        if acc_flag_sd != 2:
            age_cform = "%d;%d.%d" % (diff.years, diff.months, diff.days)
        else:
            age_cform = "%d;%d.0" % (diff.years, diff.months)
    else: 
        age_cform = "%d;0.0" % diff.years

    age_days = str(diff_days.days)
    return([age_cform if age_cform != "0;0.0" else None, age_days if age_days != "0" else None])

def format_xml_age(age_str):
    age = re.match("P(\d*)Y(\d*)M(\d*)?D?", age_str)
    years = age.group(1)
    months = age.group(2)
    if age.groups == 3:
        days = age.group(3)
    else:
        days = "0"
    return("%s;%s.%s" % (years, months, days))

def calculate_xml_days(age_str):
    age = re.match("(\d*);(\d*).(\d*)", age_str)
    years = int(age.group(1))
    months = int(age.group(2))
    days = int(age.group(3))
    out = years * 365 + months * 31 + days
    return out
