""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""
import time
import argparse

from acqdiv.parsers.CorpusConfigParser import CorpusConfigParser
from acqdiv.parsers.CorpusParserMapper import CorpusParserMapper
from acqdiv.database.DBProcessor import DBProcessor


class Loader:

    def load(self, test=True, new=False, phonbank=False):
        """Load data from source files into DB.

        Args:
            test (bool): Test DB is used.
            new (bool): Run over the new corpora as well.
            phonbank (bool): Run over the Phonbank corpora.
        """
        start_time = time.time()

        configs = [
            'Chintang.ini',
            'English_Manchester1.ini',
            'Indonesian.ini',
            'Russian.ini',
            'Cree.ini',
            'Inuktitut.ini',
            'Japanese_Miyata.ini',
            'Japanese_MiiPro.ini',
            'Nungon.ini',
            'Qaqet.ini',
            'Sesotho.ini',
            'Tuatschin.ini',
            'Turkish.ini',
            'Yucatec.ini'
        ]

        if new:
            configs += [
                'Dene.ini',
                'Ku_Waru.ini'
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

            print("{0} seconds --- Start processing: {1}".format(
                time.time() - start_time, config.split(".")[0]))

            # get corpus parser based on corpus name
            name = cfg['corpus']['corpus']
            corpus_parser_class = CorpusParserMapper.map(name)
            corpus_parser = corpus_parser_class(cfg)

            # get the corpus
            corpus = corpus_parser.parse()

            # add the corpus to the DB
            db_processor.process_corpus(corpus)

        print("%s seconds --- Finished" % (time.time() - start_time))
        print()
        print("Next, call:")

        if test:
            print("acqdiv postprocess")
        else:
            print("acqdiv postprocess -f")
        print()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    args = p.parse_args()

    loader = Loader()
    loader.load(test=args.t)


if __name__ == "__main__":
    main()
