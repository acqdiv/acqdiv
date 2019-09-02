#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main command line interface of the acqdiv package.

Invoking commands:
    acqdiv [OPTIONS] <command> [ARGS]

The following commands are supported:
    - load
    - postprocess
    - test
    - pipeline
"""
import os
import time
import acqdiv
import argparse
import unittest

from acqdiv.loader import Loader
from acqdiv.postprocessor import PostProcessor
from acqdiv.tests.systemtests.test_integrity import IntegrityTest


def load(args):
    """Run the loader."""
    start_time = time.time()
    loader = Loader()
    loader.load(
        test=not args.full
    )
    print("%s seconds --- Finished" % (time.time() - start_time))
    print()
    print("Next, call:")

    if args.full:
        print("acqdiv postprocess -f")
    else:
        print("acqdiv postprocess")
    print()


def postprocess(args):
    """Run the postprocessor."""
    start_time = time.time()
    postprocessor = PostProcessor()
    postprocessor.postprocess(
        test=not args.full,
    )
    print("%s seconds --- Finished" % (time.time() - start_time))
    print()
    print('Next, run tests:')
    print('acqdiv test')
    print('acqdiv test -i')
    print()


def test(args):
    """Run the tests."""
    test_loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()

    if args.i:
        suite = test_loader.loadTestsFromTestCase(IntegrityTest)
        runner.run(suite)
    else:
        suite = test_loader.discover('tests/unittests')
        runner.run(suite)


def pipeline(args):
    """Run the loader, postprocessor and the tests."""
    load(args)
    postprocess(args)


def get_cmd_args():
    """Get the command-line arguments."""
    parser = argparse.ArgumentParser(
                description=('Main command line interface of the '
                             'acqdiv package.'))
    subparsers = parser.add_subparsers(
        description=('For more information on the sub-commands, '
                     'run acqdiv <sub-command> -h.'))

    # command 'load'
    parser_load = subparsers.add_parser(
        'load', help='Run loader',
        description=('The loader parses the corpus files '
                     'and imports the data into a SQLite database. '
                     'By default, only the test files are parsed and '
                     'the data is imported into a test database. '
                     'To run the loader on the full database, '
                     'use the flag -f.'))
    parser_load.add_argument(
        '-f', '--full', action='store_true', help='Run on full database')

    parser_load.set_defaults(func=load)

    # command 'postprocess'
    parser_postprocess = subparsers.add_parser(
        'postprocess', help='Run postprocessor',
        description=('The postprocessor fills additional columns '
                     'in the database which contain cleaned, unified and '
                     'standardized data across the different corpora. '
                     'By default, the postprocessor is run '
                     'on the test database. '
                     'To run the postprocessor on the full database, '
                     'use the flag -f.'))
    parser_postprocess.add_argument(
        '-f', '--full', action='store_true', help='Run on full database')
    parser_postprocess.set_defaults(func=postprocess)

    # command 'test'
    parser_test = subparsers.add_parser(
        'test', help='Run tests',
        description=('By default, runs the unit tests. '
                     'To run the validation tests for the test database. '
                     'To run integrity tests for the full database, '
                     'use the flag -f.'))
    parser_test.add_argument(
        '-i', action='store_true', help='Run integrity tests on the DB')
    parser_test.set_defaults(func=test)

    # command 'pipeline'
    parser_pipeline = subparsers.add_parser(
        'pipeline', help='Run loader, postprocessor and tests',
        description='Runs the complete pipeline '
                    'by performing the same actions as the sub-commands '
                    'load, postprocess and test. '
                    'By default, all actions are executed '
                    'on the test database. '
                    'To run them on the full database, use the flag -f.')
    parser_pipeline.add_argument(
        '-f', '--full', action='store_true', help='Run on full database')

    parser_pipeline.set_defaults(func=pipeline)

    return parser.parse_args()


def main():
    here = os.path.abspath(os.path.dirname(acqdiv.__file__))
    os.chdir(here)
    args = get_cmd_args()
    args.func(args)


if __name__ == '__main__':
    main()
