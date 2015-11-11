#a skeleton xml parser subclassing the nltk childes corpus reader, to play around with
#see http://www.nltk.org/_modules/nltk/corpus/reader/childes.html

import re
from collections import defaultdict

from nltk.util import flatten
from nltk.compat import string_types

from nltk.corpus.reader.util import concat
from nltk.corpus.reader.xmldocs import XMLCorpusReader, ElementTree

from nltk.corpus.reader import NS #this is how nltk deals with the talkbank URLs everywhere
from nltk.corpus.reader import CHILDESCorpusReader

class ACQDIVCorpusReader(CHILDESCorpusReader):
    """
    Class to read in Childes XML Corpora and extract ACQDIV-specific information from them.
    """

    mortypes = set(['mortyp', 'actmor', 'tarmor'])

    def __init__(self, root, fileids, lazy=True):
        super().__init__(root, fileids, lazy)

    def morphs(self, speaker='ALL', fileids=None):
        """
        args: 
            speaker: the speaker to target
            fileids: list of corpus files to search in

        returns:
            A list of strings.
        """
        return concat([self._get_morphemes(speaker, fileid)
            for fileid in self.abspaths(fileids)])

    def _get_morphemes(self, speaker, fileid):

        xmldoc = ElementTree.parse(fileid).getroot()

        results = []

        for xmlsent in xmldoc.findall('.//{%s}u' % NS):
            xmlmorphs = xmlsent.findall('.//{%s}a' % NS) 

            for xmlmor in xmlmorphs:
                if (xmlmor.attrib.get('flavor')
                        in ACQDIVCorpusReader.mortypes):
                    morph = xmlmor.text
                else:
                    morph = ''
                results.append(morph)

        return results

def test_read(corpus_dir):
    corpus_root = corpus_dir
    corpus = ACQDIVCorpusReader(corpus_root, '.*.xml')
    return corpus

if __name__ == '__main__':
    cree = test_read('../corpora/Cree/xml')
    print(cree.morphs(cree.fileids()[0]))
