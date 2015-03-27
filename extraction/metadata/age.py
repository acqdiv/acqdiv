from datetime import datetime

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

if __name__ == "__main__":
    import sys
    print(days_between(sys.argv[1], sys.argv[2]))
