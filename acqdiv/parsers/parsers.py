""" Parsers for ACQDIV corpora, e.g. CHAT XML, Toolbox files
"""

import logging
import configparser
from configparser import ExtendedInterpolation

# main

from acqdiv.parsers.corpora.main.cree.CreeParser import CreeParser
from acqdiv.parsers.corpora.main.dene.DeneParser import DeneParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutParser import InuktitutParser
from acqdiv.parsers.corpora.main.turkish.TurkishParser import TurkishParser
from acqdiv.parsers.corpora.main.english.EnglishManchester1Parser import \
    EnglishManchester1Parser
from acqdiv.parsers.corpora.main.indonesian.IndonesianParser \
    import IndonesianParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProParser import \
    JapaneseMiiProParser
from acqdiv.parsers.corpora.main.japanese_miyata.JapaneseMiyataParser import \
    JapaneseMiyataParser
from acqdiv.parsers.corpora.main.ku_waru.KuWaruParser import KuWaruParser
from acqdiv.parsers.corpora.main.sesotho.SesothoParser import SesothoParser
from acqdiv.parsers.corpora.main.nungon.NungonParser import NungonParser
from acqdiv.parsers.corpora.main.qaqet.QaqetParser import QaqetParser
from acqdiv.parsers.corpora.main.russian.RussianParser import RussianParser
from acqdiv.parsers.corpora.main.tuatschin.TuatschinParser \
    import TuatschinParser
from acqdiv.parsers.corpora.main.yucatec.YucatecParser import YucatecParser
from acqdiv.parsers.corpora.main.chintang.ChintangParser import ChintangParser

# phonbank

from acqdiv.parsers.corpora.phonbank.arabic_kern.ArabicKernParser import \
    ArabicKernParser
from acqdiv.parsers.corpora.phonbank.arabic_kuwaiti.ArabicKuwaitiParser \
    import ArabicKuwaitiParser
from acqdiv.parsers.corpora.phonbank.berber.BerberParser import BerberParser
from acqdiv.parsers.corpora.phonbank.quichua.QuichuaParser import QuichuaParser
from acqdiv.parsers.corpora.phonbank.polish.PolishParser import PolishParser


logger = logging.getLogger('pipeline.' + __name__)


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


class SessionParser(object):
    """ Static class-level method to create a new parser instance based on session format type.
    """

    mappings = {
        'Cree': CreeParser,
        'Inuktitut': InuktitutParser,
        'Turkish': TurkishParser,
        'English_Manchester1': EnglishManchester1Parser,
        'Japanese_MiiPro': JapaneseMiiProParser,
        'Japanese_Miyata': JapaneseMiyataParser,
        'Sesotho': SesothoParser,
        'Nungon': NungonParser,
        'Yucatec': YucatecParser,
        'Arabic_Kern': ArabicKernParser,
        'Arabic_Kuwaiti': ArabicKuwaitiParser,
        'Berber': BerberParser,
        'Polish': PolishParser,
        'Quichua': QuichuaParser,
        'Tuatschin': TuatschinParser,
        'Russian': RussianParser,
        'Qaqet': QaqetParser,
        'Ku_Waru': KuWaruParser,
        'Dene': DeneParser,
        'Chintang': ChintangParser,
        'Indonesian': IndonesianParser
    }

    def __init__(self, config, file_path):
        """ Session parser initializer

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file
        """
        self.config = config
        self.file_path = file_path

    @staticmethod
    def create_parser_factory(config):
        """Create a corpus session parser based on input format type.

        Args:
            config: CorpusConfigParser

        Returns:
            A corpus-type-specific parser
        """
        format = config['corpus']['format']
        corpus = config['corpus']['corpus']

        parser = SessionParser.mappings[corpus]

        if format == "cha":
            return parser
        elif format == "toolbox":
            return lambda file_path: parser(config, file_path)
        else:
            assert 0, "Unknown format type: " + format

    def get_sha1(self):
        # TODO: get SHA1 fingerprint for each session file and write to the sessions table.
        pass

    def get_session_metadata(self):
        """ Gets session metadata for the Sessions table in the db
        """
        pass

    def next_speaker(self):
        """ Yield speakers for the Speaker table in the db
        """
        pass

    def next_utterance(self):
        """ Yield utterances for the Utterance table in the db
        """
        pass
