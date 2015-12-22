from lxml import etree

import re
import json
import os
from collections import defaultdict

from nltk.util import flatten

from nltk.corpus.reader.util import concat

from nltk.corpus.reader import NS #this is how nltk deals with the talkbank URLs everywhere

from metadata import Chat
from parsers import CorpusConfigParser as Ccp

class XMLParserMaker(object):

    def __init__(self, conf):
        self.conf = conf

    def __call__(self, cfg, fpath):
        return self.conf[cfg['corpus']](cfg, fpath)

class XMLParser(object):

    mortypes = set(['mortyp', 'mor', 'trn'])
    udict = { 'utterance_id':None,
              'starts_at':None,
              'ends_at':None,
              'speaker_id':None,
              'addressee':None,
              'sentence_type':None,
              'phonetic':None,
              'orthographic':None,
              'english':None,
              'words':None,
              'morphemes':None,
              'comments':None      }


    def __init__(self, cfg, fpath):
        self.cfg = cfg
        self.fpath = fpath
        self.metadata_parser = Chat(cfg, fpath)

    def _get_utts(self):

        xmldoc = etree.parse(self.fpath).getroot()

        for u in xmldoc.findall('.//{%s}u' % NS):

            d = XMLParser.udict.copy()
            
            words = self._get_words(u)
            info = self._get_info(u)
            
            morph = info[0]
            trans = info[1]

            d['speaker'] = u.attrib.get('who')
            d['words'] = words
            d['morphemes'] = morph
            d['english'] = trans
            d['id'] = u.attrib.get('uID')
            yield d

    def _get_words(self, u):
        raw_words = u.findall('.//{%s}w' % NS)
        words = self._word_inference(raw_words)
        return words

    def _word_inference(self, words):
        new_words = []
        for word in words:
            new_words.append(word.text)
        return new_words

    def _morpheme_inference(self, morphstring):
        return morphstring

    def _get_info(self, u):
        morph = None
        trans = None
        for a in u.findall('.//{%s}a' % NS):
            if (a.attrib.get('type')
                    == 'extension' and a.attrib.get('flavor')
                    in XMLParser.mortypes):
                morph = a.text
            elif (a.attrib.get('type') == 'coding'):
                morph = a.text
            elif (a.attrib.get('type') == 'english translation'):
                trans = a.text
            else:
                continue
        return (morph, trans)

    def get_session_metadata(self):
        return self.metadata_parser.metadata['__attrs__']

    def next_speaker(self):
        for p in self.metadata_parser.metadata['participants']:
            yield p

    def next_utterance(self):
        for u in self._get_utts():
            yield u

class CreeParser(XMLParser):

    def _word_inference(self, words):
        for w in words:
            # Specific utterances in Turkish that are not glossed <w formType="(interjection|onomatopoeia|family-specific)">...</w>
            # set target to '???'
            # set attribute 'glossed' to 'no'
            if 'type' in w.attrib and w.attrib['type'] == 'omission':
                w = None
        
        # replacements in w.text
        for w in words:
            # In ElementTree, w.text only stores the text immediately following <w>. In <w>ha<p type="drawl"/>i</w>, only 'ha' is stored as the text of <w> whereas 'i' is stored as the tail of <p>. Tags of this type are: <p> ('prosody marker'), <ca-element> ('pitch marker'), and <wk> ('word combination', marks boundaries between the elements of compounds)
            for path in ('.//p', './/ca-element', './/wk'):
                for t in w.findall(path):
                    if t.tail is not None:
                        if w.text is None:
                            w.text = t.tail
                        else:
                            w.text += t.tail
            # CHAT www, xxx, yyy all have an attribute "untranscribed/unintelligible" in XML; unify text to '???'
            if 'untranscribed' in w.attrib:
                w.text = '???'
                # three corpora don't have glosses for xxx words -> mark word
                #if corpus_name in ['Turkish', 'Japanese_MiiPro', 'Yucatec']:
                #    w.attrib['glossed'] = 'no'
            # other replacements
            if w.text:
                # Cree: where the orthography tier is missing <w> is not empty but contains 'missingortho' -> remove this
                w.text = re.sub('missingortho', '', w.text)
                # Cree: replace "zéro" (= zero morpheme) by more standard "Ø"
                w.text = re.sub('zéro', 'Ø', w.text)
                # Sometimes words may be partially untranscribed (-xxx, xxx-, -xxx-) - transform this, too
                w.text = re.sub('\-?xxx\-?', '???', w.text)
                # only in Cree: morpheme boundaries in <w> are indicated by '_' -> remove these, segments are also given in the morphology tiers. Other corpora can have '_' in <w>, too, but there it's meaningful (e.g. for concatenating the parts of a book title treated as a single word), so only check Cree!
                w.text = re.sub('_', '', w.text)
        # EOF string replacements
                                    
        # transcriptions featuring a contrast between actual and target pronunciation: go through words, create an attribute "target" (initially identical to its text), and set it as appropriate. "target" is taken up later again when all content is written to the corpus dic. 
        for w in words:
            
            # Note that in ElementTree, w.text only stores the text immediately following <w>. In <w>al<shortening>pha</shortening>bet</w>, only 'al' is stored as the text of <w> whereas bet' is stored as the tail of <shortening>. Therefore, actual and target pronunciation have to be assembled step by step in most cases. 
            if w.text is None:
                w.text = ''
            w_actual = w.text
            w_target = w.text

            # fragments: actual pronunciation remains, target pronunciation is '???' as with untranscribed words. No glosses. This may occasionally be overwritten by a <replacement> further down.
            if 'type' in w.attrib and w.attrib['type'] == 'fragment':
                w.attrib['target'] = '???'
                w.attrib['glossed'] = 'no'
                continue
                        
            # shortenings, e.g. <g><w>wo<shortening>rd</shortening>s</w></g>: 'wos' = actual pronunciation, 'words' = target pronunciation
            # shortenings have to be processed before replacements because a target string with no shortenings may still be classified as a replaced form 
            for s in w.findall('shortening'):
                if s.text is not None:
                    w_target += s.text
                if s.tail is not None:
                    w_target += s.tail
                    w_actual += s.tail
                w.remove(s)
            w.text = w_actual
            w.attrib['target'] = w_target
        # EOF actual vs target    
            
        # replacements, e.g. <g><w>burred<replacement><w>word</w></replacement></w></g>
        # these require an additional loop over <w> in <u> because there may be shortenings within replacements
        for i in range(0, len(words)):
            r = words[i].find('replacement')
            if r is not None:
                rep_words = r.findall('w')

                # go through words in replacement
                for j in range(0, len(rep_words)):
                    # check for morphology
                    mor = rep_words[j].find('mor')
                    # first word: transfer content and any morphology to parent <w> in <u>
                    if j== 0:
                        words[i].attrib['target'] = rep_words[0].attrib['target']
                        if mor is not None:
                            words[i].insert(0, mor)
                    # all further words: insert new empty <w> under parent of last known <w> (= <u> or <g>), put content and morphology there
                    else:
                        w = etree.Element('w')
                        w.text = ''
                        w.attrib['target'] = rep_words[j].attrib['target']
                        if mor is not None:
                            w.insert(0, mor)
                        parent_map[words[i]].insert(i+j, w)
                        
                # w.attrib['target'] = '_'.join(rep_w.attrib['target'] for rep_w in r.findall('w'))
                words[i].remove(r)
                
                # example for shortening within complex replacement in Japanese MiiPro (aprm19990722.u287), processing step by step:
                # (1) initial XML string
                #   <w>kitenee<replacement><w>kite</w><w><shortening>i</shortening>nai</w></replacement></w>
                # (2) add targets to all <w>
                #   <w target="kitenee">kitenee<replacement><w target="kite">kite</w><w target="nai"><shortening>i</shortening>nai</w></replacement></w>
                # (3) reset target for shortening  
                #   <w target="kitenee">kitenee<replacement><w target="kite">kite</w><w target="inai"><shortening>i</shortening>nai</w></replacement></w>
                # (4) remove shortening tag
                #   <w target="kitenee">kitenee<replacement><w target="kite">kite</w><w target="inai">nai</w></replacement></w>
                # (5) reset target for w to replacement
                #   <w target="kite">kitenee<replacement><w target="kite">kite</w><w target="inai">nai</w></replacement></w>
                # (6) insert new empty word with target = second element of replacement
                #   <w target="kite">kitenee<replacement><w target="kite">kite</w><w target="inai">nai</w></replacement></w><w target="inai"/>
                # (7) remove replacement tag
                #   <w target="kite">kitenee</w><w target="inai"/>
        
        # EOF replacements

        words = filter(lambda w: w != None, words)
        return [w.text for w in words]

def test_read(config, fileid):
    corpus = CreeParser(config, fileid)
    return corpus

if __name__ == '__main__':
    conf = Ccp()
    conf.read('Cree.ini')
    corpus = test_read(conf, '../corpora/Cree/xml/01-A1-2005-03-08ms.xml')

    with open('test.json', 'w') as tf:
        #tf.write('Participants:\n')
        #for p in corpus.next_speaker():
        #    json.dump(p, tf)
        tf.write('Metadata:\n')
        json.dump(corpus.get_session_metadata(), tf)
        tf.write('\n\n######################\n\nUtterances:\n')
        for u in corpus.next_utterance():
            json.dump(u, tf)
            tf.write('\n')
