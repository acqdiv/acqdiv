#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main command line interface of the acqdiv package.

Invoking commands:
    acqdiv [OPTIONS] <command> [ARGS]

The following commands are supported:
    - load
"""
import os
import time
import acqdiv
import argparse

from acqdiv.loader import Loader


def load(args):
    """Run the loader."""
    start_time = time.time()
    loader = Loader()

    if args.cfg:
        loader.load(cfg_path=args.cfg)
    else:
        loader.load()

    print("%s seconds --- Finished" % (time.time() - start_time))


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
        'load', help='Load the data into the database.',
        description=('The loader parses the corpus files '
                     'and imports the data into a SQLite database. '
                     'By default, only the test files are parsed and '
                     'the data is imported into a test database. '
                     'To run the loader on the full database, '
                     'use the flag -f.'))
    parser_load.add_argument(
        '-c', '--cfg', help="Specify a path to a custom ini file.")

    parser_load.set_defaults(func=load)

    return parser.parse_args()


def main():
    here = os.path.abspath(os.path.dirname(acqdiv.__file__))
    os.chdir(here)
    args = get_cmd_args()
    args.func(args)


if __name__ == '__main__':
    main()
