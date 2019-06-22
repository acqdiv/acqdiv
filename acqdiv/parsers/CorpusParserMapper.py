# main

from acqdiv.parsers.corpora.main.chintang.ChintangCorpusParser \
    import ChintangCorpusParser
from acqdiv.parsers.corpora.main.cree.CreeCorpusParser \
    import CreeCorpusParser
from acqdiv.parsers.corpora.main.dene.DeneCorpusParser \
    import DeneCorpusParser
from acqdiv.parsers.corpora.main.english.EnglishCorpusParser \
    import EnglishCorpusParser
from acqdiv.parsers.corpora.main.indonesian.IndonesianCorpusParser \
    import IndonesianCorpusParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutCorpusParser \
    import InuktitutCorpusParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProCorpusParser \
    import JapaneseMiiProCorpusParser
from acqdiv.parsers.corpora.main.japanese_miyata.JapaneseMiyataCorpusParser \
    import JapaneseMiyataCorpusParser
from acqdiv.parsers.corpora.main.ku_waru.KuWaruCorpusParser \
    import KuWaruCorpusParser
from acqdiv.parsers.corpora.main.nungon.NungonCorpusParser \
    import NungonCorpusParser
from acqdiv.parsers.corpora.main.qaqet.QaqetCorpusParser \
    import QaqetCorpusParser
from acqdiv.parsers.corpora.main.russian.RussianCorpusParser \
    import RussianCorpusParser
from acqdiv.parsers.corpora.main.sesotho.SesothoCorpusParser \
    import SesothoCorpusParser
from acqdiv.parsers.corpora.main.tuatschin.TuatschinCorpusParser \
    import TuatschinCorpusParser
from acqdiv.parsers.corpora.main.turkish.TurkishCorpusParser \
    import TurkishCorpusParser
from acqdiv.parsers.corpora.main.yucatec.YucatecCorpusParser \
    import YucatecCorpusParser

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


class CorpusParserMapper:

    mappings = {
        # main
        'Chintang': ChintangCorpusParser,
        'Cree': CreeCorpusParser,
        'Dene': DeneCorpusParser,
        'English_Manchester1': EnglishCorpusParser,
        'Indonesian': IndonesianCorpusParser,
        'Inuktitut': InuktitutCorpusParser,
        'Japanese_MiiPro': JapaneseMiiProCorpusParser,
        'Japanese_Miyata': JapaneseMiyataCorpusParser,
        'Ku_Waru': KuWaruCorpusParser,
        'Nungon': NungonCorpusParser,
        'Qaqet': QaqetCorpusParser,
        'Russian': RussianCorpusParser,
        'Sesotho': SesothoCorpusParser,
        'Tuatschin': TuatschinCorpusParser,
        'Turkish': TurkishCorpusParser,
        'Yucatec': YucatecCorpusParser,

        # phonbank
        'Arabic_Kern': ArabicKernParser,
        'Arabic_Kuwaiti': ArabicKuwaitiParser,
        'Berber': BerberParser,
        'Polish': PolishParser,
        'Quichua': QuichuaParser,
    }

    @staticmethod
    def map(name):
        return CorpusParserMapper.mappings[name]
