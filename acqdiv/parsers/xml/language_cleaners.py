import importlib
import os


def init():
    mods = []
    for d,ss,fs in os.walk(os.path.dirname(__file__)):
        for f in fs:
            if (f.endswith('.py') and not
            (f == 'xml_cleaner.py' or f == 'language_cleaners.py')):
                mods.append(f)
    for mod in mods:
        mname = os.path.basename(mod)
        globals[mname] = importlib.import_module(mname, package=xml)


init()
