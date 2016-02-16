from lxml import etree

import re
import importlib
import json
import os
import sys
import logging
from collections import defaultdict

from metadata import Chat

class XMLParserFactory(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.CorpusParser = importlib.import_module(self.cfg['paths']['parser'])
        self.parser_cls = eval(("self.CorpusParser." + 
            self.cfg['paths']['parser_name']), globals(), locals())

    def __call__(self, fpath):
        return self.parser_cls(self.cfg, fpath)

class XMLParser(object):

    udict = { 'utterance_id':None,
              'session_id_fk':None,
              'start_raw':None,
              'end_raw':None,
              'speaker_id':None,
              'addressee':None,
              'sentence_type':None,
              'phonetic':None,
              'phonetic_target':None,
              'translation':None,
              'comments':None,
              'warning':None          }

    mordict = { 'morphemes':None,
                'gloss_raw':None,
                'pos_raw':None    }


    def __init__(self, cfg, fpath):
        self.cfg = cfg
        self.fpath = fpath
        self.sname = os.path.basename(fpath).split(".")[0]
        self.metadata_parser = Chat(cfg, fpath)

    def _get_utts(self):

        xmldoc = etree.parse(self.fpath).getroot()

        for elem in xmldoc.iter():
            # remove prefixed namespaces
            try:
                elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
                tag = elem.tag
                attrib = elem.attrib
            except TypeError:
                print(type(elem))

        for u in xmldoc.findall('.//u'):
            
            #uwm = utterance - words - morphemes
            uwm = {}
            d = XMLParser.udict.copy()
            
            words = self._get_words(u)
            uwm['words'] = words

            anno = self._get_annotations(u)
            morph = anno[0]
            trans = anno[1]
            comment = anno[2]

            uwm['morphology'] = XMLParser.mordict.copy()

            for tier in morph:
                uwm['morphology'][self.cfg['morphology_tiers'][tier]
                        ] = morph[tier]

            d['translation'] = trans
            d['comments'] = comment

            phonetic = self._get_phonetic(u)
            d['phonetic'] = phonetic[0]
            d['phonetic_target'] = phonetic[1]

            ts = self._get_timestamps(u)
            d['start_raw'] = ts[0]
            d['end_raw'] = ts[1]

            d['speaker_id'] = u.attrib.get('who')
            d['sentence_type'] = self._get_sentence_type(u)
            d['utterance_id'] = u.attrib.get('uID')

            uwm['utterance'] = d

            yield uwm

    def _get_words(self, u):
        clean_u = self._clean_groups(u)
        raw_words = u.findall('.//w')
        words = self._word_inference(raw_words, u)
        return words

    def _clean_groups(self, u):
        groups = u.findall('.//g')
        map(self._clean_repetitions, groups)
        map(self._clean_retracings, groups)
        map(self._clean_guesses, groups)
        return u

    def _clean_repetitions(self, group):
        reps = group.find('r')
        if reps:
            ws = group.findall('.//w')
            for i in range(int(reps.attrib['times'])-1):
                for w in words:
                    group[len(ws)-1] = copy.deepcopy(w)

    def _clean_retracings(self, group):
        words = group.findall('.//w')
        retracings = group.find('k[@type="retracing"]')
        retracings_wc = group.find('k[@type="retracing with correction"]')
        if (retracings is not None) or (retracings_wc is not None):
            # we can't do checks for corpus name here so
            # just use Turkish / MiiPro as default
            # and override for miyata
            for w in words: 
                w.attrib['glossed'] = 'ahead'

    def _clean_guesses(self, group):
        target_guess = g.find('.//ga[@type="alternative"]')
        if target_guess is not None:
            words[0].attrib['target'] = target_guess.text

        guesses = g.find('k[@type="best guess"]')
        if guesses is not None:
            for w in words:
                w.attrib['transcribed'] = 'insecure'

    def _word_inference(self, words, u):
        new_words = []
        for word in words:
            new_words.append(word.text)
        return new_words

    def _morphology_inference(self, morphstring):
        return morphstring

    def _get_phonetic(self, u):
        return (None, None)

    def _get_annotations(self, u):
        morph = {}
        trans = None
        comment = None
        for a in u.findall('.//a'):
            for tier in self.cfg['morphology_tiers']:
                if (a.attrib.get('type') == 'extension'
                        and a.attrib.get('flavor') == tier):
                    morph[tier] = a.text
            if (a.attrib.get('type') == 'english translation'):
                trans = a.text
            if (a.attrib.get('type') in ['comments', 'actions', 'explanation']):
                comment = a.text
        return (morph, trans, comment)

    def _get_sentence_type(self, u):
        st_raw = u.find('t').attrib.get('type')
        stype = self.cfg['correspondences'][st_raw]
        return stype

    def _get_timestamps(self, u):
        return (None, None)

    def get_session_metadata(self):
        return self.metadata_parser.metadata['__attrs__']

    def next_speaker(self):
        for p in self.metadata_parser.metadata['participants']:
            yield p

    def next_utterance(self):
        for u in self._get_utts():
            yield u['utterance'], u['words'], u['morphemes']


##################################################

def test_read(config, fileid):
    corpus = CreeParser.CreeParser(config, fileid)
    return corpus

if __name__ == '__main__':
    from parsers import CorpusConfigParser as Ccp
    import CreeParser
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
