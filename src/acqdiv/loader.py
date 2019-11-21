""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""
import os
from configparser import ConfigParser, ExtendedInterpolation

from acqdiv.parsers.corpus_parser_mapper import CorpusParserMapper
from acqdiv.database.processor import DBProcessor


class Loader:

    @staticmethod
    def load(cfg_path='config.ini'):
        """Load data from source files into DB.

        Args:
            cfg_path (str): Path to the config file.
        """
        print('Reading config file:', os.path.abspath(cfg_path))
        cfg = ConfigParser(interpolation=ExtendedInterpolation())
        cfg.read(cfg_path)

        db_dir = cfg['.global']['db_dir']
        db_processor = DBProcessor(db_dir=db_dir)

        for section in cfg.sections():
            # ignore sections starting with a dot
            if not section.startswith('.'):
                # get corpus parser based on corpus name
                corpus_parser_class = CorpusParserMapper.map(section)
                data = dict(cfg.items(section))
                corpus_parser = corpus_parser_class(data)

                # get the corpus
                corpus = corpus_parser.parse()

                # add the corpus to the DB
                db_processor.insert_corpus(corpus)


def main():
    Loader.load()


if __name__ == "__main__":
    main()
