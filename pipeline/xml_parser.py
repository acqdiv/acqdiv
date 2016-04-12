import copy
import importlib
import itertools
import json
import logging
import os
import pdb
import re
import sys
import traceback

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

    logging.basicConfig(filemode='w')
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('errors.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    @staticmethod
    def creadd(location, key, value):
        if key not in location.keys() or location[key] is None:
            location[key] = value
        else:
            if value in location[key]:
                pass
            else:
                location[key] += '; ' + value

    @staticmethod
    def word_index_up(ls, llen, idx, parent):
        idx += 1
        if idx >= llen:
            new_word = etree.Element('w')
            act = etree.SubElement(new_word, 'actual')
            tar = etree.SubElement(new_word, 'target')
            act.text = '???'
            tar.text = '???'
            new_word.attrib['dummy'] = 'misaligned morphemes'
            parent.insert(llen, new_word)
            ls.insert(llen, new_word)
            llen += 1
        return idx, llen

    def __init__(self, cfg, fpath):
        self.cfg = cfg
        self.fpath = fpath
        self.sname = os.path.basename(fpath).split('.')[0]
        self.metadata_parser = Chat(cfg, fpath)

    def _get_utts(self, debug=False):

        xmldoc = etree.parse(self.fpath).getroot()

        for elem in xmldoc.iter():
            # remove prefixed namespaces
            try:
                elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
                tag = elem.tag
                attrib = elem.attrib
            except TypeError:
                pass

        for u in xmldoc.getiterator('u'):

            try:
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

                self._process_morphology(uwm)
                self._morphology_inference(uwm)
                self._clean_morphemes(uwm)
                uwm['utterance']['pos_raw'] = self._concat_mor_tier(
                        'pos_raw', uwm['words'])
                uwm['utterance']['gloss_raw'] = self._concat_mor_tier(
                        'gloss_raw', uwm['words'])
                uwm['utterance']['morpheme'] = self._concat_mor_tier(
                        'morpheme', uwm['words'])

                uwm['words'] = self._clean_words(uwm['words'])
                uwm['utterance']['utterance_raw'] = ' '.join(
                        [w['word'] for w in uwm['words']])


                yield uwm

            except Exception as e:
                XMLParser.logger.warn("Aborted processing of utterance {} "
                        "in file {} with error: {}\nStacktrace: {}".format(
                            u.attrib.get('uID'), self.fpath, repr(e),
                            traceback.format_exc()))

    def _debug_xml(self):

        xmldoc = etree.parse(self.fpath)
        root = xmldoc.getroot()

        for elem in root.iter():
            # remove prefixed namespaces
            try:
                elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
                tag = elem.tag
                attrib = elem.attrib
            except TypeError:
                pass

        for u in xmldoc.iterfind('.//u'):

            try:
                self._clean_xml_utterance(u)
            except Exception as e:
                #u.getparent().remove(u)
                XMLParser.logger.warn("Aborted processing of utterance {} "
                        "in file {} with error: {}\nStacktrace: {}".format(
                            u.attrib.get('uID'), self.fpath, repr(e),
                            traceback.format_exc()))

        #with open('{}_clean.xml'.format(self.fpath), 'w') as out:
        xmldoc.write('{}_clean.xml'.format(self.fpath),
                encoding='utf-8', pretty_print=False)
            

    def _clean_xml_utterance(self, u):

        if self.cfg['morphemes']['repetitions_glossed'] == 'yes':
            self._word_inference(u)
            self._clean_groups(u)
            self._process_morphology(u)
        else:
            self._word_inference(u)
            self._process_morphology(u)
            self._clean_groups(u)
        self._morphology_inference(u)
        self._add_morphology_warnings(u)
        self._remove_junk(u)

    def _remove_junk(self, u):
        pass

    def _concat_mor_tier(self, tier, morphlist):
        return ' '.join(['-'.join([m for m in map(
            lambda x:
                x[tier] if x[tier] is not None 
                else '???', mword)])
            for mword in morphlist])

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
        return new_mword

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
        if self.cfg['repetitions_glossed'] == 'yes':
            words = self._word_inference(raw_words, u)
            self._process_morphology(u)
        else:
            self._process_morphology(u)
            words = self._word_inference(raw_words, u)
        return words

    def _clean_groups(self, u):
        for group in u.iterfind('.//g'):

            parent = group.getparent()
            idx = parent.index(group)

            self._clean_repetitions(group)
            self._clean_retracings(group, u)
            self._clean_guesses(group)
            for w in group.iterfind('.//w'):
                parent.insert(idx, w)
                idx += 1
            parent.remove(group)

    def _clean_repetitions(self, group):
        reps = group.find('r')
        if reps is not None:
            ws = group.findall('.//w')
            for i in range(int(reps.attrib['times'])-1):
                for w in ws:
                    group.insert(len(ws)-1, copy.deepcopy(w))

    def _clean_retracings(self, group, u):
        retracings = group.find('k[@type="retracing"]')
        retracings_wc = group.find('k[@type="retracing with correction"]')

        if retracings is not None:
            group_ws = group.findall('w')
            for w in group_ws:
                elems_with_same_text = [e for e in u.iterfind('.//w')
                        if e.find('actual').text == w.find('actual').text]
                for elem in elems_with_same_text:
                    mor = elem.find('mor')
                    # if there is <mor>, insert below the retraced word
                    if mor is not None:
                        w.append(copy.deepcopy(mor))
                        if 'warning' in w.attrib:
                            w.attrib['warning'] = re.sub('not glossed; search ahead',
                                    '', w.attrib['warning'])
                            if w.attrib['warning'] == '':
                                del w.attrib['warning']
                        w.find('target').text = elem.find('target').text
                        break
                if w.find('mor') is None:
                    if 'warning' in w.attrib:
                        w.attrib['warning'] = re.sub('; search ahead',
                                '', w.attrib['warning'])
                if 'glossed' in w.attrib:
                    del w.attrib['glossed']

        elif retracings_wc is not None:
            group_ws = group.findall('w')
            u_ws = u.findall('.//w')
            base_index = u_ws.index(group_ws[-1]) + 1
            max_index = base_index + len(group_ws)
            for i,j in zip(range(base_index, max_index), itertools.count()):
                if u_ws[i].find('mor') is not None: 
                    mor = etree.SubElement(group_ws[j], 'mor')
                    mor.text = u_ws[i].find('mor').text
                    if 'warning' in w.attrib:
                        re.sub('not glossed; search ahead', '', 
                                group_ws[j].attrib['warning'])
                else:
                    if 'warning' in group_ws[j].attrib:
                        re.sub('; search ahead', '', group_ws[j].attrib['warning'])
                group_ws[j].find('target').text = u_ws[i].find('target').text
                if 'glossed' in group_ws[j].attrib:
                    del group_ws[j].attrib['glossed']

    def _clean_guesses(self, group):
        words = group.findall('.//w')
        target_guess = group.find('.//ga[@type="alternative"]')
        if target_guess is not None:
            words[0].find('target').text = target_guess.text

        guesses = group.find('k[@type="best guess"]')
        if guesses is not None:
            for w in words:
                w.attrib['transcribed'] = 'insecure'

    def _word_inference(self, u):
        words = u.findall('.//w')
        self._restructure_words(words)
        self._clean_word_text(words)
        self._clean_fragments_and_omissions(words)
        self._clean_shortenings(words)
        self._clean_replacements(words)
        self._mark_retracings(u)
        self._add_word_warnings(words)
        #words = filter(lambda w: w != None, words)

        #return [{'full_word': w.text, 'full_word_target': w.attrib['target'],
        #    'warning': w.attrib['warning']} for w in words]

    def _restructure_words(self, words):
        for w in words:
            actual = etree.SubElement(w, 'actual')
            target = etree.SubElement(w, 'target')
            if w.text is not None:
                actual.text = w.text
            else:
                actual.text = ''
            target.text = ''
            w.text = ''

    def _clean_word_text(self, words):
        for w in words:
            wt = w.find('actual')
            for path in ('.//p', './/ca-element', './/wk'):
                for t in w.findall(path):
                    if t.tail is not None:
                        if wt.text is None:
                            wt.text = t.tail
                        else:
                            wt.text += t.tail
                    w.remove(t)
            if wt.text:
                # Sometimes words may be partially untranscribed
                # (-xxx, xxx-, -xxx-) - transform this to unified ???
                wt.text = re.sub('\-?xxx\-?', '???', wt.text)
            if 'untranscribed' in w.attrib:
                wt.text = '???'

    def _clean_fragments_and_omissions(self, words):
        for w in words:
            if 'type' in w.attrib:
                if w.attrib['type'] == 'omission':
                    w = None
                elif w.attrib['type'] == 'fragment':
                    w.find('target').text = '???'
                    w.attrib['warning'] = 'not glossed'
        
    def _clean_shortenings(self, words):
        for w in words:

            w_actual = w.find('actual')
            w_target = w.find('target')
            w_target.text = w_actual.text

            for s in w.findall('shortening'):
                if s.text is not None:
                    w_target.text += s.text
                if s.tail is not None:
                    w_target.text += s.tail
                    w_actual.text += s.tail
                w.remove(s)

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
                        words[i].find('target').text = rep_words[0].find('target').text
                        if mor is not None:
                            words[i].append(mor)
                    # all further words: insert new empty <w> under parent of
                    # last known <w> (= <u> or <g>),
                    # put content and morphology there
                    else:
                        w = etree.Element('w')
                        w_act = etree.SubElement(w, 'actual')
                        w_tar = etree.SubElement(w, 'target')
                        w_tar.text = rep_words[j].find('target').text
                        if mor is not None:
                            w.append(mor)
                        words.insert(i+j, w)
                        
                #words[i].attrib['target'] = '_'.join(rep_w.attrib['target'] 
                #        for rep_w in r.findall('w'))
                words[i].remove(r)
                for k in range(1,rep_len+1):
                    del words[i+k]

    def _mark_retracings(self, u):
        for group in u.iterfind('.//g'):
            retracings = group.find('k[@type="retracing"]')
            retracings_wc = group.find('k[@type="retracing with correction"]')
            if (retracings is not None) or (retracings_wc is not None):
                words = group.findall('.//w')
                for w in words: 
                    w.attrib['glossed'] = 'ahead'
                    XMLParser.creadd(w.attrib, 'warning', 'not glossed; search ahead')
        
    def _add_word_warnings(self, words):
        for w in words:
            if 'glossed' in w.attrib:
                if w.attrib['glossed'] == 'no':
                    XMLParser.creadd(w.attrib, 'warning', 'not glossed')
                elif w.attrib['glossed'] == 'repeated':
                    XMLParser.creadd(w.attrib, 'warning', 'not glossed; repeat')
                elif w.attrib['glossed'] == 'ahead':
                    XMLParser.creadd(w.attrib, 'warning', 'not glossed; search ahead')
            if 'transcribed' in w.attrib and w.attrib['transcribed'] == 'insecure':
                XMLParser.creadd(w.attrib, 'warning', 'transcription insecure')            
            #if 'warning' not in w.attrib:
            #    w.attrib['warning'] = ''

    def _process_morphology(self, u):
        pass

    def _morphology_inference(self, u):
        pass

    def _add_morphology_warnings(self, u):
        if u.find('.//mor') is None:
            XMLParser.creadd(u.attrib, 'warning', 'not glossed')
        else:
            for w in u.findall('.//w'):
                #print('alignment problem in ' + self.fpath + ', utterance ' + str(utterance_index) + ': general word tier <w> has
                #+ str(length_words) + ' words vs ' + str(length_morphology) + ' in "mor" (= morphology)')
                if w.find('./mor') is None:
                    XMLParser.creadd(u.attrib, 'warning', 'broken alignment full_word : segments/glosses')
                    break

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
