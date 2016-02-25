import copy
import importlib
import itertools
import json
import logging
import os
import pdb
import re
import sys

from collections import defaultdict
from lxml import etree
from metadata import Chat


class XMLParserFactory(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.CorpusParser = importlib.import_module(self.cfg['paths']['parser'])
        self.parser_cls = eval(('self.CorpusParser.' + 
            self.cfg['paths']['parser_name']), globals(), locals())

    def __call__(self, fpath):
        return self.parser_cls(self.cfg, fpath)

class XMLParser(object):

    udict = { 'source_id':None,
              'session_id_fk':None,
              'start_raw':None,
              'end_raw':None,
              'speaker_label':None,
              'addressee':None,
              'sentence_type':None,
              'translation':None,
              'comment':None,
              'warning':None          }

    mordict = { 'morphemes':None,
                'gloss_raw':None,
                'pos_raw':None    }


    @staticmethod
    def creadd(location, key, value):
        if key not in location.keys() or location[key] is None:
            location[key] = value
        else:
            location[key] += '; ' + value

    def __init__(self, cfg, fpath):
        self.cfg = cfg
        self.fpath = fpath
        self.sname = os.path.basename(fpath).split('.')[0]
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
                pass

        for u in xmldoc.iterfind('.//u'):
            
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
            d['comment'] = comment

            ts = self._get_timestamps(u)
            d['start_raw'] = ts[0]
            d['end_raw'] = ts[1]

            d['speaker_label'] = u.attrib.get('who')
            d['sentence_type'] = self._get_sentence_type(u)
            d['source_id'] = u.attrib.get('uID')

            d['corpus'] = self.cfg['corpus']['corpus']
            d['language'] = self.cfg['corpus']['language']

            uwm['utterance'] = d

            uwm['morphemes'] = self._morphology_inference(uwm)
            uwm['morphemes'] = self._clean_morphemes(uwm['morphemes'])

            uwm['words'] = self._clean_words(uwm['words'])
            uwm['utterance']['utterance_raw'] = ' '.join(
                    [w['word'] for w in uwm['words']])


            yield uwm

    def _clean_words(self, words):
        new_words = []
        for raw_word in words:
            word = {}
            for k in raw_word:
                if k in self.cfg['json_mappings_words']:
                    label = self.cfg['json_mappings_words'][k]
                    word[label] = raw_word[k]
                else:
                    word[k] = raw_word[k]
                    if word[k] == "":
                        word[k] = None
            word['word'] = word[self.cfg['json_mappings_words']['word']]
            new_words.append(word)
        return new_words

    def _clean_morphemes(self, mors):
        new_mors = []
        for mword in mors:
            new_mword = []
            for raw_morpheme in mword:
                morpheme = {}
                for k in raw_morpheme:
                    if k in self.cfg['json_mappings_morphemes']:
                        label = self.cfg['json_mappings_morphemes'][k]
                        morpheme[label] = raw_morpheme[k]
                    else:
                        morpheme[k] = raw_morpheme[k]
                new_mword.append(morpheme)
            new_mors.append(new_mword)
        return new_mors

    def _clean_utterance(self, raw_u):

        utterance = {}
        for k in raw_u:
            if k in self.config['json_mappings_utterance']:
                label = self.config['json_mappings_utterance'][k]
                utterance[label] = raw_u[k]
            else:
                utterance[k] = raw_u[k]
        return utterance

    def _get_words(self, u):
        u = self._clean_groups(u)
        raw_words = u.findall('.//w')
        words = self._word_inference(raw_words, u)
        return words

    def _clean_groups(self, u):
        for group in u.iterfind('.//g'):
            self._clean_repetitions(group)
            self._clean_retracings(group)
            self._clean_guesses(group)
        return u

    def _clean_repetitions(self, group):
        reps = group.find('r')
        if reps is not None:
            ws = group.findall('.//w')
            for i in range(int(reps.attrib['times'])-1):
                for w in ws:
                    group.insert(len(ws)-1, copy.deepcopy(w))

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
        words = group.findall('.//w')
        target_guess = group.find('.//ga[@type="alternative"]')
        if target_guess is not None:
            words[0].attrib['target'] = target_guess.text

        guesses = group.find('k[@type="best guess"]')
        if guesses is not None:
            for w in words:
                w.attrib['transcribed'] = 'insecure'

    def _add_word_warnings(self, words):
        new_words = []
        for w in words:
            try:
                if 'glossed' in w.attrib:
                    if w.attrib['glossed'] == 'no':
                        XMLParser.creadd(w.attrib, 'warning', 'not glossed')
                    elif w.attrib['glossed'] == 'repeated':
                        XMLParser.creadd(w.attrib, 'warning', 'not glossed; repeat')
                    elif w.attrib['glossed'] == 'ahead':
                        XMLParser.creadd(w.attrib, 'warning', 'not glossed; search ahead')
                if 'transcribed' in w.attrib and w.attrib['transcribed'] == 'insecure':
                    XMLParser.creadd(w.attrib, 'warning', 'transcription insecure')            
                if 'warning' not in w.attrib:
                    w.attrib['warning'] = ''
                new_words.append(w)
            except TypeError:
                pass
        return new_words

    def _word_inference(self, words, u):
        words = self._clean_word_text(words)
        words = self._clean_fragments_and_omissions(words)
        words = self._clean_shortenings(words)
        words = self._clean_replacements(words)
        words = self._add_word_warnings(words)
        words = filter(lambda w: w != None, words)

        return [{'full_word': w.text, 'full_word_target': w.attrib['target'],
            'warning': w.attrib['warning']} 
            for w,i in zip(words, itertools.count())]

    def _clean_word_text(self, words):
        for w in words:
            for path in ('.//p', './/ca-element', './/wk'):
                for t in w.findall(path):
                    if t.tail is not None:
                        if w.text is None:
                            w.text = t.tail
                        else:
                            w.text += t.tail
            if w.text:
                # Sometimes words may be partially untranscribed
                # (-xxx, xxx-, -xxx-) - transform this to unified ???
                w.text = re.sub('\-?xxx\-?', '???', w.text)
            if 'untranscribed' in w.attrib:
                w.text = '???'
        return words

    def _clean_fragments_and_omissions(self, words):
        for w in words:
            if 'type' in w.attrib:
                if 'type' == 'omission':
                    w = None
                elif 'type' == 'fragment':
                    w.attrib['target'] = '???'
                    w.attrib['glossed'] = 'no'
        return words
    
    def _clean_shortenings(self, words):
        for w in words:

            if w.text is None:
                w.text = ''
            w_actual = w.text
            w_target = w.text

            for s in w.findall('shortening'):
                if s.text is not None:
                    w_target += s.text
                if s.tail is not None:
                    w_target += s.tail
                    w_actual += s.tail
                w.remove(s)

            w.text = w_actual
            w.attrib['target'] = w_target

        return words

    def _clean_replacements(self, words):
        # replacements, e.g. 
        # <g><w>burred<replacement><w>word</w></replacement></w></g>
        # these require an additional loop over <w> in <u>,
        # because there may be shortenings within replacements
        js = itertools.count()
        for i in js:
            if i >= len(words):
                break
            r = words[i].find('replacement')
            if r is not None:
                rep_words = r.findall('w')
                rep_len = len(rep_words)

                # go through words in replacement
                for j in range(rep_len):
                    # check for morphology
                    mor = rep_words[j].find('mor')
                    # first word: transfer content 
                    # and any morphology to parent <w> in <u>
                    if j == 0:
                        words[i].attrib['target'] = rep_words[0].attrib['target']
                        if mor is not None:
                            words[i].insert(0, mor)
                    # all further words: insert new empty <w> under parent of
                    # last known <w> (= <u> or <g>),
                    # put content and morphology there
                    else:
                        w = etree.Element('w')
                        w.text = ''
                        w.attrib['target'] = rep_words[j].attrib['target']
                        if mor is not None:
                            w.insert(0, mor)
                        words.insert(i+j, w)
                        
                #words[i].attrib['target'] = '_'.join(rep_w.attrib['target'] 
                #        for rep_w in r.findall('w'))
                words[i].remove(r)
                for k in range(1,rep_len+1):
                    del words[i+k]
        return words

    def _morphology_inference(self, u):
        pass

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
            if (a.attrib.get('type') in ['comment', 'actions', 'explanation']):
                comment = a.text
        return morph, trans, comment

    def _get_sentence_type(self, u):
        st_raw = u.find('t').attrib.get('type')
        stype = self.cfg['correspondences'][st_raw]
        return stype

    def _get_timestamps(self, u):
        ts = u.find('.//media')
        if ts != None:
            return ts.attrib.get('start'), ts.attrib.get('end')
        else:
            return None, None

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
