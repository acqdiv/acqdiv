import os
import shutil
from collections import defaultdict
from copy import copy

# we import re to make it available to corpus-specific code which is
# defined running `exec` (https://docs.python.org/3.2/library/functions.html#exec)
# in Corpus.code
import re

from pyacqdiv.util import existing_dir, utf8, read_csv
from pyacqdiv.lib.chat import chat


STATUS = {num: label for num, label in enumerate([
    'none', 'initialized', 'cleaned'])}


def identity(s):
    return s


# The globals (i.e. imports) available in corpus specific code:
CORPUS_SPECIFIC_GLOBALS = {'re': re}

# A dict of (function name, default implementation) pairs.
# When one of these names is defined in a corpus specific code.py module, this definition
# will take precedence over the default implementation given here.
# Care should be taken to add only names here, which do not conflict with any other
# global name.
CORPUS_SPECIFIC_FUNCTIONS = {
    # used to normalize a session filename when copying to input:
    'clean_filename': identity,
    # used to normalize a single line in a session file when cleaning.
    'clean_chat_line': identity,
}


class Corpus(object):
    """
    Expected directory layout for the cleaning process:

    cleaning/
    ├── <corpus.id>
    │   ├── cfg
    │   │   ├── code.py
    │   │   ├── ids.tsv
    │   │   ├── participants.csv
    │   │   └── replacements.csv
    │   ├── input/
    │   └── output/

    <corpus.id>/cfg/code.py is expected to be a python module that can be run via
    `exec`, thereby (optionally) defining two functions `clean_chat_line` and
    `clean_filename`, both operating upon a unicode string.
    """
    def __init__(self, id_, cfg):
        self.id = id_
        self.cfg = cfg
        self._participants = {}
        self._ids = defaultdict(list)
        self._replacements = []
        self._code = {}

    #
    # commands: The following methods are registered as commands with the acqdiv cli.
    #
    def status(self):
        """
        workflow status is determined by checking the existence of intermediate
        processing directories.

        Note: For diagnostic purposes we want to leave processing directories intact
        even when the command that created them eventually failed, e.g. because one
        file couldn't be processed. Thus, even a failed clean will result in a status
        of "cleaned".

        :return: Workflow status of the corpus.
        """
        num = 0
        if os.path.exists(self.output_path()):
            num = 2
        elif os.path.exists(self.input_path()):
            num = 1
        return num, STATUS[num]

    def config(self):
        """
        :return: The configuration dict of the corpus.
        """
        return ''.join('\n%s: %s' % (k, self.cfg[k]) for k in sorted(self.cfg.keys()))

    def setup(self):
        """Copy files from copora directory to cleaning/input and rewrite to UTF-8.

        :return: Number of session files copied to input.
        """
        assert existing_dir(self.input_path())
        count = 0
        for dir_path, subdir_list, file_list in os.walk(self.cfg['src']):
            for fname in file_list:
                if fname.startswith('.'):
                    continue
                dst = self.input_path(self.code['clean_filename'](fname))
                shutil.copy(os.path.join(dir_path, fname), dst)
                utf8(dst)
                count += 1
        return count

    def clear_input(self):
        """Removes the input and output directories for corpus cleaning, thereby
        resetting the workflow status.
        """
        shutil.rmtree(self.input_path(), ignore_errors=True)
        self.clear_output()

    def clear_output(self):
        """Removes the output directory for corpus cleaning.
        """
        shutil.rmtree(self.output_path(), ignore_errors=True)

    def clean(self):
        """Clean all session files of a corpus.
        """
        if self.status() == 0:
            self.setup()

        assert existing_dir(self.output_path())
        for filename in os.listdir(self.input_path()):
            if not filename.startswith('.'):
                with open(self.output_path(filename), 'w', encoding='utf8') as outfile:
                    outfile.write(self.clean_session(filename))

    #
    # internal helpers
    #
    @property
    def code(self):
        """Try to import corpus-specifc code.

        :return: dict with (possibly) corpus-specifc function or the defaults.
        """
        if not self._code:
            # Note: we must copy here, to make sure we don't change the module global!
            self._code = copy(CORPUS_SPECIFIC_FUNCTIONS)
            code_path = self.cfg_path('code.py')
            if os.path.exists(code_path):
                code = open(code_path, encoding='utf8').read()
                _locals = {}
                exec(code, CORPUS_SPECIFIC_GLOBALS, _locals)
                for name in CORPUS_SPECIFIC_FUNCTIONS:
                    if _locals.get(name):
                        self._code[name] = _locals[name]
        return self._code

    @property
    def participants(self):
        if not self._participants:
            if os.path.exists(self.cfg_path('participants.csv')):
                self._participants = {
                    r[0]: r[1] for r in read_csv(
                        self.cfg_path('participants.csv'), skip_header=True, quotechar='"')}
        return self._participants

    @property
    def replacements(self):
        if not self._replacements:
            if os.path.exists(self.cfg_path('replacements.csv')):
                for row in read_csv(self.cfg_path('replacements.csv')):
                    if len(row) != 2:
                        raise ValueError("Replacements input longer than two columns")
                    self._replacements.append(tuple(row))
        return self._replacements

    @property
    def ids(self):
        if not self._ids:
            if os.path.exists(self.cfg_path('ids.tsv')):
                for row in read_csv(
                        self.cfg_path('ids.tsv'), skip_header=True, delimiter='\t'):
                    self._ids[row[0]].append("@ID:\t%s|" % "|".join(row[1:-1]))
        return self._ids

    def cleaning_path(self, *comps):
        return os.path.join(
            existing_dir(os.path.join(self.cfg['cleaning_dir'], self.id)), *comps)

    def input_path(self, *comps):
        return os.path.join(os.path.join(self.cleaning_path(), '.input'), *comps)

    def output_path(self, *comps):
        return os.path.join(os.path.join(self.cleaning_path(), '.output'), *comps)

    def cfg_path(self, *comps):
        return os.path.join(os.path.join(self.cleaning_path(), 'cfg'), *comps)

    def clean_session(self, filename):
        lines = []
        body = False
        for line in open(self.input_path(filename), 'r', encoding='utf8').readlines():
            if line.strip() in ['', '*', '%']:
                continue

            if not body and not line.startswith('@'):
                # body starts at first non-empty non-'@' line, right?
                body = True

            if body and not line.lower().replace(' ', '').startswith('@end'):
                lines.append(line)

        return chat(
            self.cfg['iso_code'],
            self.participants[filename],
            self.ids[filename],
            filename,
            list(map(self.code['clean_chat_line'], lines)))
