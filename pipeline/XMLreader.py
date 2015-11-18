# a skeleton xml parser subclassing the nltk childes corpus reader, to play around with
# see http://www.nltk.org/_modules/nltk/corpus/reader/childes.html

import re
import json
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

    mortypes = set(['mortyp', 'mor', 'trn'])

    def __init__(self, root, fileids, lazy=True):
        super().__init__(root, fileids, lazy)

    def utterances(self, fileids):
        return concat([self._get_utts(fileid)
            for fileid in self.abspaths(fileids)])

    def _get_utts(self, fileid):

        xmldoc = ElementTree.parse(fileid).getroot()

        results = []

        for u in xmldoc.findall('.//{%s}u' % NS):
            d = {   'speaker':None,
                    'words':None,
                    'morphstring':None,
                    'english':None,
                    'id':None           }

            words = []
            trans = None
            morph = None

            for w in u.findall('.//{%s}w' % NS):
                words.append(w.text)

            for a in u.findall('.//{%s}a' % NS):
                if (a.attrib.get('type')
                        == 'extension' and a.attrib.get('flavor')
                        in ACQDIVCorpusReader.mortypes):
                    morph = a.text
                elif (a.attrib.get('type') == 'coding'):
                    morph = a.text
                elif (a.attrib.get('type') == 'english translation'):
                    trans = a.text
                else:
                    continue


            d['speaker'] = u.attrib.get('who')
            d['words'] = words
            d['morphstring'] = morph
            d['english'] = trans
            d['id'] = u.attrib.get('uID')
            results.append(d)

        return results

    def _s_and_m(self, speaker='ALL', fileids=None):
        # :^)
        return zip(self.sents(fileids),
                self.morphs(fileids))

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
                if (xmlmor.attrib.get('type')
                        == 'extension' and xmlmor.attrib.get('flavor')
                        in ACQDIVCorpusReader.mortypes):
                    morph = xmlmor.text
                elif (xmlmor.attrib.get('type') == 'coding'):
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
    corpus = test_read('../corpora/test/')
    acqdiv = {}
    for subcorpus in corpus.fileids():
        scname = subcorpus.split('.')[0]
        acqdiv[scname] = corpus.utterances(subcorpus)
    with open('test.json', 'w') as tf:
        json.dump(acqdiv, tf)
