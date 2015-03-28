from datetime import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta

def childes_age_format(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    #return abs((d2 - d1).days)
    diff = relativedelta(d2, d1)
    return("%d;%d.%d" % (diff.years, diff.months, diff.days))

if __name__ == "__main__":
    import sys
    print(childes_age_format(sys.argv[1], sys.argv[2]))


