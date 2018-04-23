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
    loader.set_logger(level_i=args.i, supressing_formatter=args.s)
    loader.load(test=not args.f)


def postprocess(args):
    """Run the postprocessor."""
    postprocessor.set_logger(suppressing_formatter=args.s)
    postprocessor.postprocess(test=not args.f)


def test(args):
    """Run the tests."""
    # get test suite creators
    # for test_integrity the unittest loader
    test_loader = unittest.TestLoader()
    # for test_regression the nose loader because there are no test classes
    # but only test methods which the unittest loader cannot find
    nose_test_loader = nose.loader.TestLoader()

    if args.f:
        # get a test suite of all test cases for the production DB
        suite = test_loader.loadTestsFromTestCase(ValidationTest_ProductionDB)
    else:
        # get a test suite of all test cases for the development DB
        suite = test_loader.loadTestsFromTestCase(ValidationTest_DevDB)
        nose_suite = nose_test_loader.loadTestsFromModule(test_regression)
        nose_runner = nose.core.TextTestRunner()
        nose_runner.run(nose_suite)

    runner = unittest.TextTestRunner()
    runner.run(suite)


def pipeline(args):
    """Run the loader, postprocessor and the tests."""
    load(args)
    postprocess(args)
    test(args)


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
        '-f', action='store_true', help='Run on full database')
    parser_load.add_argument(
        '-s', action='store_true', help='Use suppressing formatter for log')
    parser_load.add_argument(
        '-i', action='store_true', help='Set logging to INFO level')
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
        '-f', action='store_true', help='Run on full database')
    parser_postprocess.add_argument(
        '-s', action='store_true', help='Use suppressing formatter for log')
    parser_postprocess.set_defaults(func=postprocess)

    # command 'test'
    parser_test = subparsers.add_parser(
        'test', help='Run tests',
        description=('By default, runs the regression tests and '
                     'integrity tests for the test database. '
                     'To run integrity tests for the full database, '
                     'use the flag -f.'))
    parser_test.add_argument(
        '-f', action='store_true', help='Run on full database')
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
        '-f', action='store_true', help='Run on full database')
    parser_pipeline.add_argument(
        '-s', action='store_true', help='Use suppressing formatter for log')
    parser_pipeline.add_argument(
        '-i', action='store_true', help='Set logging to INFO level')
    parser_pipeline.set_defaults(func=pipeline)

    return parser.parse_args()


def main():
    os.chdir(os.path.abspath(os.path.dirname(acqdiv.__file__)))
    args = get_cmd_args()
    args.func(args)


if __name__ == '__main__':
    main()
