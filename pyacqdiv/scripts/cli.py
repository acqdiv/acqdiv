"""
Main command line interface of the pyacqdiv package.

Like programs such as git, this cli splits its functionality into sub-commands
(see e.g. https://docs.python.org/2/library/argparse.html#sub-commands).
The rationale behind this is that while a lot of different tasks may be triggered using
this cli, most of them require common configuration.

The basic invocation looks like

    acqdiv [OPTIONS] <command> [args]

One important option is `--corpora`, which takes a comma-separated list of corpus
identifiers. This option controls which corpora the command should act upon. If not
given, all corpora listed in the config file corpora.ini will be acted upon.

<command> is used as key to lookup a python callable in the dict of available commands.
A callable suitable as command must have the following signature:

    def cmd(corpus, *args):
        pass

The cli will then loop over all specified copora and invoke

    cmd(corpus, *args)

on each, where `args` is a (possibly empty) list of additional arguments passed on
the command line.
"""
import os
import sys
import argparse
from configparser import ConfigParser

from pyacqdiv import util
from pyacqdiv.corpus import Corpus


# The following dict is used to register callables as named commands.
COMMANDS = {
    'status': Corpus.status,
    'config': Corpus.config,
    'setup': Corpus.setup,
    'clean': Corpus.clean,
    'clear_input': Corpus.clear_input,
    'clear_output': Corpus.clear_output,
}


def main():
    parser = argparse.ArgumentParser(
        description="""Main command line interface of the pyacqdiv package.
Used to run commands on specific or all configured (default) corpora.""",
        epilog="Use '%(prog)s help <cmd>' to get help about individual commands.")
    parser.add_argument(
        "--src-dir",
        help="directory holding the raw corpus data",
        default=util.pkg_path('..', 'corpora'))
    parser.add_argument(
        "--cleaning-dir",
        help="directory for the cleaning process",
        default=util.pkg_path('..', 'cleaning'))
    parser.add_argument("--verbosity", help="increase output verbosity")
    parser.add_argument("--corpora", help="comma-separated list of corpus IDs")
    parser.add_argument('command', help='|'.join(COMMANDS.keys()))
    parser.add_argument('args', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    cfg = ConfigParser()
    cfg['DEFAULT'] = {'src_dir': args.src_dir, 'cleaning_dir': args.cleaning_dir}
    cfg.read(os.path.join(args.src_dir, 'corpora.ini'))

    if args.command == 'help':
        # As help text for individual commands we simply re-use the docstrings of the
        # callables registered for the command:
        print(COMMANDS[args.args[0]].__doc__)
        sys.exit(0)

    cmd = COMMANDS[args.command]

    # Now we loop over the corpus identifiers, either specified for the --corpora option
    # or as given in corpora.ini:
    for cid in (util.split_words(args.corpora) if args.corpora else cfg.sections()):
        # Instantiate a Corpus object, passing in the config from corpora.ini:
        corpus = Corpus(cid, dict(cfg.items(cid)))

        # Call the function registered for the command:
        res = cmd(corpus, *args.args)
        print('%s: %s' % (cid, res if res is not None else 'ok'))

    sys.exit(0)
