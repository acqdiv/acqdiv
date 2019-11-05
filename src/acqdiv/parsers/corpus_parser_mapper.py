from acqdiv.parsers.corpora.main.chintang.corpus_parser \
    import ChintangCorpusParser
from acqdiv.parsers.corpora.main.cree.corpus_parser \
    import CreeCorpusParser
from acqdiv.parsers.corpora.main.dene.corpus_parser \
    import DeneCorpusParser
from acqdiv.parsers.corpora.main.english.corpus_parser \
    import EnglishCorpusParser
from acqdiv.parsers.corpora.main.indonesian.corpus_parser \
    import IndonesianCorpusParser
from acqdiv.parsers.corpora.main.inuktitut.corpus_parser \
    import InuktitutCorpusParser
from acqdiv.parsers.corpora.main.japanese_miipro.corpus_parser \
    import JapaneseMiiProCorpusParser
from acqdiv.parsers.corpora.main.japanese_miyata.corpus_parser \
    import JapaneseMiyataCorpusParser
from acqdiv.parsers.corpora.main.ku_waru.corpus_parser \
    import KuWaruCorpusParser
from acqdiv.parsers.corpora.main.nungon.corpus_parser \
    import NungonCorpusParser
from acqdiv.parsers.corpora.main.qaqet.corpus_parser \
    import QaqetCorpusParser
from acqdiv.parsers.corpora.main.russian.corpus_parser \
    import RussianCorpusParser
from acqdiv.parsers.corpora.main.sesotho.corpus_parser \
    import SesothoCorpusParser
from acqdiv.parsers.corpora.main.tuatschin.corpus_parser \
    import TuatschinCorpusParser
from acqdiv.parsers.corpora.main.turkish.corpus_parser \
    import TurkishCorpusParser
from acqdiv.parsers.corpora.main.yucatec.corpus_parser \
    import YucatecCorpusParser


class CorpusParserMapper:

    mappings = {
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
    }

    @staticmethod
    def map(name):
        return CorpusParserMapper.mappings[name]
