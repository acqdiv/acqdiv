""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""
import argparse

from acqdiv.ini.CorpusConfigParser import CorpusConfigParser
from acqdiv.parsers.CorpusParserMapper import CorpusParserMapper
from acqdiv.database.DBProcessor import DBProcessor


class Loader:

    def load(self, test=True, phonbank=False):
        """Load data from source files into DB.

        Args:
            test (bool): Test DB is used.
            phonbank (bool): Run over the Phonbank corpora.
        """
        configs = [
            'Chintang.ini',
            'Cree.ini',
            'English_Manchester1.ini',
            'Indonesian.ini',
            'Inuktitut.ini',
            'Japanese_MiiPro.ini',
            'Japanese_Miyata.ini',
            'Ku_Waru.ini',
            'Nungon.ini',
            'Qaqet.ini',
            'Russian.ini',
            'Sesotho.ini',
            'Tuatschin.ini',
            'Turkish.ini',
            'Yucatec.ini',
        ]

        if phonbank:

            base_path = 'Phonbank/'

            configs = [
                base_path + 'Arabic_Kuwaiti.ini',
                base_path + 'Arabic_Kern.ini',
                base_path + 'Berber.ini',
                base_path + 'Polish.ini',
                base_path + 'Quichua.ini'
            ]

        db_processor = DBProcessor(test=test)

        for config in configs:
            cfg = CorpusConfigParser()
            cfg.read("ini/"+config)

            # get corpus parser based on corpus name
            name = cfg['corpus']['corpus']
            corpus_parser_class = CorpusParserMapper.map(name)
            corpus_parser = corpus_parser_class(cfg)

            # get the corpus
            corpus = corpus_parser.parse()

            # add the corpus to the DB
            db_processor.insert_corpus(corpus)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    args = p.parse_args()

    loader = Loader()
    loader.load(test=args.t)


if __name__ == "__main__":
    main()
