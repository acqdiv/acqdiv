import configparser
from configparser import ExtendedInterpolation


class CorpusConfigParser(configparser.ConfigParser):
    """ Config parser for ACQDIV corpus-specific .ini configuration files
    """
    def optionxform(self, optionstr):
        return optionstr

    def __init__(self):
        """ We subclass Python's default config parser and use our own delimiter and extended interpolation.
        """
        super().__init__(delimiters=["=="], interpolation=ExtendedInterpolation())

    def read(self, config, encoding=None):
        super().read(config, encoding)
