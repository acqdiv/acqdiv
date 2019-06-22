# main

from acqdiv.parsers.corpora.main.chintang.ChintangSessionParser \
    import ChintangSessionParser
from acqdiv.parsers.corpora.main.cree.CreeSessionParser \
    import CreeSessionParser
from acqdiv.parsers.corpora.main.dene.DeneSessionParser \
    import DeneSessionParser
from acqdiv.parsers.corpora.main.english.EnglishManchester1SessionParser \
    import EnglishManchester1SessionParser
from acqdiv.parsers.corpora.main.indonesian.IndonesianSessionParser \
    import IndonesianSessionParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutSessionParser \
    import InuktitutSessionParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProSessionParser \
    import JapaneseMiiProSessionParser
from acqdiv.parsers.corpora.main.japanese_miyata.JapaneseMiyataSessionParser \
    import JapaneseMiyataSessionParser
from acqdiv.parsers.corpora.main.ku_waru.KuWaruSessionParser \
    import KuWaruSessionParser
from acqdiv.parsers.corpora.main.nungon.NungonSessionParser \
    import NungonSessionParser
from acqdiv.parsers.corpora.main.qaqet.QaqetSessionParser \
    import QaqetSessionParser
from acqdiv.parsers.corpora.main.russian.RussianSessionParser \
    import RussianSessionParser
from acqdiv.parsers.corpora.main.sesotho.SesothoSessionParser \
    import SesothoSessionParser
from acqdiv.parsers.corpora.main.tuatschin.TuatschinSessionParser \
    import TuatschinSessionParser
from acqdiv.parsers.corpora.main.turkish.TurkishSessionParser \
    import TurkishSessionParser
from acqdiv.parsers.corpora.main.yucatec.YucatecSessionParser \
    import YucatecSessionParser

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
        'Chintang': ChintangSessionParser,
        'Cree': CreeSessionParser,
        'Dene': DeneSessionParser,
        'English_Manchester1': EnglishManchester1SessionParser,
        'Indonesian': IndonesianSessionParser,
        'Inuktitut': InuktitutSessionParser,
        'Japanese_MiiPro': JapaneseMiiProSessionParser,
        'Japanese_Miyata': JapaneseMiyataSessionParser,
        'Ku_Waru': KuWaruSessionParser,
        'Nungon': NungonSessionParser,
        'Qaqet': QaqetSessionParser,
        'Russian': RussianSessionParser,
        'Sesotho': SesothoSessionParser,
        'Tuatschin': TuatschinSessionParser,
        'Turkish': TurkishSessionParser,
        'Yucatec': YucatecSessionParser,

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
