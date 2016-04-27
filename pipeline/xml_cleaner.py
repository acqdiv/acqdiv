import copy
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

class XMLCleaner(object):

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

    @staticmethod
    def find_text(parent, child):
        se = parent.find(child)
        return se.text if se is not None else None

    @staticmethod
    def find_xpath(parent, xpexpr):
        ses = parent.xpath(xpexpr)
        return ses[0] if len(ses) != 0 else None

    def __init__(self, cfg, fpath):
        self.cfg = cfg
        self.fpath = fpath
        self.sname = os.path.basename(fpath).split('.')[0]
        #self.metadata_parser = Chat(cfg, fpath)

    def _clean_xml(self):

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
                XMLCleaner.logger.warn("Aborted processing of utterance {} "
                        "in file {} with error: {}\nStacktrace: {}".format(
                            u.attrib.get('uID'), self.fpath, repr(e),
                            traceback.format_exc()))
                u.getparent().remove(u)

        return xmldoc

    def _debug_xml(self):
        xmld = self._clean_xml()
        sys.stdout.write(etree.tostring(xmld, encoding='unicode', pretty_print=True))

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
        self._restructure_metadata(u)
        self._remove_junk(u)

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
        for fw in words:
            r = fw.find('replacement')
            if r is not None:
                rep_words = r.findall('w')
                rep_len = len(rep_words)
                wp = fw.getparent()
                i = wp.index(fw)

                # go through words in replacement
                for j in range(rep_len):
                    # check for morphology
                    mor = rep_words[j].find('mor')
                    # first word: transfer content 
                    # and any morphology to parent <w> in <u>
                    if j == 0:
                        fw.find('target').text = rep_words[0].find('target').text
                        if mor is not None:
                            fw.append(mor)
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
                        wp.insert(i+j, w)
                        
                #fw.attrib['target'] = '_'.join(rep_w.attrib['target'] 
                #        for rep_w in r.findall('w'))
                fw.remove(r)

    def _mark_retracings(self, u):
        for group in u.iterfind('.//g'):
            retracings = group.find('k[@type="retracing"]')
            retracings_wc = group.find('k[@type="retracing with correction"]')
            if (retracings is not None) or (retracings_wc is not None):
                words = group.findall('.//w')
                for w in words: 
                    w.attrib['glossed'] = 'ahead'
                    XMLCleaner.creadd(w.attrib, 'warning', 'not glossed; search ahead')
        
    def _add_word_warnings(self, words):
        for w in words:
            if 'glossed' in w.attrib:
                if w.attrib['glossed'] == 'no':
                    XMLCleaner.creadd(w.attrib, 'warning', 'not glossed')
                elif w.attrib['glossed'] == 'repeated':
                    XMLCleaner.creadd(w.attrib, 'warning', 'not glossed; repeat')
                elif w.attrib['glossed'] == 'ahead':
                    XMLCleaner.creadd(w.attrib, 'warning', 'not glossed; search ahead')
            if 'transcribed' in w.attrib and w.attrib['transcribed'] == 'insecure':
                XMLCleaner.creadd(w.attrib, 'warning', 'transcription insecure')            
            #if 'warning' not in w.attrib:
            #    w.attrib['warning'] = ''

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
                    if 'warning' in group_ws[j].attrib:
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

    def _process_morphology(self, u):
        pass

    def _morphology_inference(self, u):
        pass

    def _add_morphology_warnings(self, u):
        if u.find('.//mor') is None:
            XMLCleaner.creadd(u.attrib, 'warning', 'not glossed')
        else:
            for w in u.findall('.//w'):
                #print('alignment problem in ' + self.fpath + ', utterance ' + str(utterance_index) + ': general word tier <w> has
                #+ str(length_words) + ' words vs ' + str(length_morphology) + ' in "mor" (= morphology)')
                if w.find('./mor') is None:
                    XMLCleaner.creadd(u.attrib, 'warning', 'broken alignment full_word : segments/glosses')
                    break

    def _restructure_metadata(self, u):
        for a in u.findall('a'):
            if a.attrib['type'] == 'extension':
                ntag = a.attrib['flavor']
                del a.attrib['flavor']
            else:
                ntag = a.attrib['type']
                if ' ' in ntag:
                    ntag = ntag.split()[0]
            a.tag = ntag
            del a.attrib['type']

        stype = u.find('t')
        if stype is not None:
            stype.attrib['type'] = \
                    self.cfg['correspondences'][stype.attrib.get('type')]

        timestamp = u.find('time')
        if timestamp is not None:
            timestamp.attrib['start'] = timestamp.text
            timestamp.text = ''
            timestamp.tag = 'media'

    def _remove_junk(self, u):
        pass

    def clean(self):
        return self._clean_xml()

if __name__ == '__main__':
    print("Sorry, there's nothing here!")