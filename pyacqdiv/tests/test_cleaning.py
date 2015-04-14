import os

from pyacqdiv.tests.util import WithTempDir


SESSION = """\
@Begin
@Header
with second line
%something
@End
"""

CFG = {
    'code.py': """
def clean_filename(fname):
    return fname.rstrip(".txt")

def clean_chat_line(s):
    return re.sub("something", "else", s)
""",
    'ids.tsv': """\
filename	language	corpus	code	age	sex	group	SES	role	education	custom	name
SESSION	ike	inuktitut	LOU					Mother			Louisa
""",
    'participants.csv': """\
"filename","@Participants:"
"SESSION","ALI Alec Target_Child, DAN Daniel Brother, LOU Louisa Mother"
""",
    'replacements.csv': """\
"@Portion: ","@Portion:"
"@Entererer:","@Enterer:"
"""
}


class Tests(WithTempDir):
    def setUp(self):
        WithTempDir.setUp(self)
        os.makedirs(self.tmp_path('cleaning', 'test', 'cfg'))
        os.makedirs(self.tmp_path('corpora', 'Test', 'cha'))

        with open(self.tmp_path('corpora', 'Test', 'cha', 'SESSION.txt'), 'w') as fp:
            fp.write(SESSION)

        for fname, content in CFG.items():
            with open(self.tmp_path('cleaning', 'test', 'cfg', fname), 'w') as fp:
                fp.write(content)

    def test_workflow(self):
        from pyacqdiv.corpus import Corpus

        corpus = Corpus(
            'test',
            dict(
                src=self.tmp_path('corpora', 'Test', 'cha'),
                cleaning_dir=self.tmp_path('cleaning'),
                iso_code='tst'))
        self.assertEquals(corpus.status()[0], 0)
        self.assertEquals(corpus.setup(), 1)
        self.assertEquals(corpus.status()[0], 1)
        self.assertTrue(os.path.exists(corpus.input_path('SESSION')))
        corpus.clean()
        out = corpus.output_path('SESSION')
        self.assertTrue(os.path.exists(out))
        out = open(out).read()
        self.assertIn('else', out)
        self.assertNotIn('second line', out)
        corpus.clear_input()
        self.assertEquals(corpus.status()[0], 0)
