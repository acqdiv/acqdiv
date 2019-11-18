""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""
import argparse
from configparser import ConfigParser, ExtendedInterpolation

from acqdiv.parsers.corpus_parser_mapper import CorpusParserMapper
from acqdiv.database.processor import DBProcessor


class Loader:

    @staticmethod
    def load(test=True, cfg_path='config.ini'):
        """Load data from source files into DB.

        Args:
            test (bool): Test DB is used.
            cfg_path (str): Path to the config file.
        """
        db_processor = DBProcessor(test=test)
        cfg = ConfigParser(interpolation=ExtendedInterpolation())
        cfg.read(cfg_path)

        for section in cfg.sections():
            # ignore sections starting with a dot
            if not section.startswith('.'):
                # get corpus parser based on corpus name
                corpus_parser_class = CorpusParserMapper.map(section)
                data = dict(cfg.items(section))
                corpus_parser = corpus_parser_class(data, disable_pbar=test)

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
