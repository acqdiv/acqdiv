# main

from acqdiv.parsers.corpora.main.chintang.ChintangParser \
    import ChintangParser
from acqdiv.parsers.corpora.main.cree.CreeParser \
    import CreeParser
from acqdiv.parsers.corpora.main.dene.DeneParser \
    import DeneParser
from acqdiv.parsers.corpora.main.english.EnglishManchester1Parser \
    import EnglishManchester1Parser
from acqdiv.parsers.corpora.main.indonesian.IndonesianParser \
    import IndonesianParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutParser \
    import InuktitutParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProParser \
    import JapaneseMiiProParser
from acqdiv.parsers.corpora.main.japanese_miyata.JapaneseMiyataParser \
    import JapaneseMiyataParser
from acqdiv.parsers.corpora.main.ku_waru.KuWaruParser \
    import KuWaruParser
from acqdiv.parsers.corpora.main.nungon.NungonParser \
    import NungonParser
from acqdiv.parsers.corpora.main.qaqet.QaqetParser \
    import QaqetParser
from acqdiv.parsers.corpora.main.russian.RussianParser \
    import RussianParser
from acqdiv.parsers.corpora.main.sesotho.SesothoParser \
    import SesothoParser
from acqdiv.parsers.corpora.main.tuatschin.TuatschinParser \
    import TuatschinParser
from acqdiv.parsers.corpora.main.turkish.TurkishParser \
    import TurkishParser
from acqdiv.parsers.corpora.main.yucatec.YucatecParser \
    import YucatecParser

# phonbank

from acqdiv.parsers.corpora.phonbank.arabic_kern.ArabicKernParser \
    import ArabicKernParser
from acqdiv.parsers.corpora.phonbank.arabic_kuwaiti.ArabicKuwaitiParser \
    import ArabicKuwaitiParser
from acqdiv.parsers.corpora.phonbank.berber.BerberParser \
    import BerberParser
from acqdiv.parsers.corpora.phonbank.polish.PolishParser \
    import PolishParser
from acqdiv.parsers.corpora.phonbank.quichua.QuichuaParser \
    import QuichuaParser


class ParserMapper:

    mappings = {
        # main
        'Chintang': ChintangParser,
        'Cree': CreeParser,
        'Dene': DeneParser,
        'English_Manchester1': EnglishManchester1Parser,
        'Indonesian': IndonesianParser,
        'Inuktitut': InuktitutParser,
        'Japanese_MiiPro': JapaneseMiiProParser,
        'Japanese_Miyata': JapaneseMiyataParser,
        'Ku_Waru': KuWaruParser,
        'Nungon': NungonParser,
        'Qaqet': QaqetParser,
        'Russian': RussianParser,
        'Sesotho': SesothoParser,
        'Tuatschin': TuatschinParser,
        'Turkish': TurkishParser,
        'Yucatec': YucatecParser,

        # phonbank
        'Arabic_Kern': ArabicKernParser,
        'Arabic_Kuwaiti': ArabicKuwaitiParser,
        'Berber': BerberParser,
        'Polish': PolishParser,
        'Quichua': QuichuaParser,
    }

    @staticmethod
    def map(name):
        return ParserMapper.mappings[name]
