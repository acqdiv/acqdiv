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
import acqdiv
import argparse
import unittest
import nose

from acqdiv import loader, postprocessor
from acqdiv.tests.test_integrity import ValidationTest_DevDB
from acqdiv.tests.test_integrity import ValidationTest_ProductionDB
from acqdiv.tests import test_regression


def load(args):
    """Run the loader."""
    loader.set_logger(
        level_i=args.info_log_level,
        supressing_formatter=args.suppress_log_formatter)
    loader.load(
        test=not args.full,
        catch_errors=args.catch_errors,
        xml=args.xml,
        new=args.new_corpora,
        phonbank=args.phonbank_corpora
    )


def postprocess(args):
    """Run the postprocessor."""
    postprocessor.set_logger(
        suppressing_formatter=args.suppress_log_formatter
    )
    postprocessor.postprocess(
        test=not args.full,
        xml=args.xml
    )


def test(args):
    """Run the tests."""
    # get test suite creators
    # unittest version
    test_loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()
    # nose version
    nose_test_loader = nose.loader.TestLoader()
    nose_runner = nose.core.TextTestRunner()

    # run unittests
    suite = test_loader.discover('tests/unittests')
    runner.run(suite)

    if args.f:
        # get a test suite of all test cases for the production DB
        suite = test_loader.loadTestsFromTestCase(ValidationTest_ProductionDB)
        runner.run(suite)

    if args.o:
        # get a test suite of all test cases for the development DB
        suite = test_loader.loadTestsFromTestCase(ValidationTest_DevDB)
        runner.run(suite)
        nose_suite = nose_test_loader.loadTestsFromModule(test_regression)
        nose_runner.run(nose_suite)


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
    parser_load.add_argument(
        '-s', '--suppress-log-formatter',
        action='store_true', help='Use suppressing formatter for log')
    parser_load.add_argument(
        '-i', '--info-log-level',
        action='store_true', help='Set logging to INFO level')
    parser_load.add_argument(
        '-e', '--catch-errors', action='store_true', help='Catch errors')
    parser_load.add_argument(
        '-x', '--xml', action='store_true', help='Run the XML parsers')
    parser_load.add_argument(
        '-n', '--new-corpora', action='store_true',
        help='Run over the new corpora as well.')
    parser_load.add_argument(
        '-p', '--phonbank-corpora', action='store_true',
        help='Run over the Phonbank corpora as well.')

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
    parser_postprocess.add_argument(
        '-s', '--suppress-log-formatter',
        action='store_true', help='Use suppressing formatter for log')
    parser_postprocess.add_argument(
        '-x', '--xml', action='store_true',
        help='Loader was run with xml parsers')
    parser_postprocess.set_defaults(func=postprocess)

    # command 'test'
    parser_test = subparsers.add_parser(
        'test', help='Run tests',
        description=('By default, runs the unit tests. '
                     'To run the validation tests for the test database. '
                     'To run integrity tests for the full database, '
                     'use the flag -f.'))
    parser_test.add_argument(
        '-f', action='store_true', help='Run validation tests on full DB')
    parser_test.add_argument(
        '-o', action='store_true', help='Run old tests. Deprecated soon.')
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
    parser_pipeline.add_argument(
        '-s', '--suppress-log-formatter',
        action='store_true', help='Use suppressing formatter for log')
    parser_pipeline.add_argument(
        '-i', '--info-log-level',
        action='store_true', help='Set logging to INFO level')
    parser_pipeline.add_argument(
        '-e', '--catch-errors', action='store_true', help='Catch errors')
    parser_pipeline.add_argument(
        '-x', '--xml', action='store_true', help='Run the XML parsers')
    parser_pipeline.add_argument(
        '-n', '--new-corpora', action='store_true',
        help='Run over the new corpora as well.')
    parser_pipeline.add_argument(
        '-p', '--phonbank-corpora', action='store_true',
        help='Run over the Phonbank corpora as well.')

    parser_pipeline.set_defaults(func=pipeline)

    return parser.parse_args()


def main():
    here = os.path.abspath(os.path.dirname(acqdiv.__file__))
    os.chdir(here)
    args = get_cmd_args()
    args.func(args)


if __name__ == '__main__':
    main()
