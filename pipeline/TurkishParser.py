# -*- coding: utf-8 -*-

import copy
import re
import sys
import itertools

from lxml import etree
from XMLParser import XMLParser

class TurkishParser(XMLParser):

    def _word_inference(self, words, u):
        for w in words:

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
                w.attrib['glossed'] = 'no'
                # three corpora don't have glosses for xxx words -> mark word
                #if corpus_name in ['Turkish', 'Japanese_MiiPro', 'Yucatec']:
                #    w.attrib['glossed'] = 'no'
            # other replacements
            if w.text:
                # Sometimes words may be partially untranscribed (-xxx, xxx-, -xxx-) - transform this, too
                w.text = re.sub('\-?xxx\-?', '???', w.text)
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

            if 'formType' in w.attrib and w.attrib['formType'] in ['interjection', 'onomatopoeia', 'family-specific']:
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
                    if j == 0:
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
                        words.insert(i+j, w)
                        
                # w.attrib['target'] = '_'.join(rep_w.attrib['target'] for rep_w in r.findall('w'))
                words[i].remove(r)

        for w in words:
            try:
                if w.attrib['glossed'] == 'no':
                    w.attrib['warning'] = 'not glossed'
            except KeyError:
                w.attrib['warning'] = ''

        words = filter(lambda w: w != None, words)
        return [{"full_word": w.text, "full_word_target": w.attrib['target'],
            "utterance_id_fk": u.attrib.get('uID'), 
            "word_id": (u.attrib.get('uID') + 'w' + str(i)),
            "warning": w.attrib['warning']} 
            for w,i in zip(words, itertools.count())]

    def _get_phonetic(self, u):

        out = []

        for tier in ['actual', 'model']:

            block = u.find('.//' + tier)
            if block != None:
                words = []
                for w in block.findall('pw'):
                    word_concatenated = ''
                    for child in w:
                        if child.tag == 'ph':
                            word_concatenated += child.text
                        elif child.tag == 'ss' and child.attrib['type'] == '1':
                            word_concatenated += 'ʼ'
                        #elif child.tag == 'ss' and child.attrib['type'] != '1':
                        #    print('unknown Cree type', child.attrib['type'], '- update export script!')
                        #elif child.tag != 'ss':
                        #    print('unknown Cree phonetic element', child.tag, '- update export script!')
                        else:
                            pass
                    words.append(word_concatenated)
                out.append(' '.join(words))
            else:
                out.append(None)

        return out

    def _morphology_inference(self, u):
        morphemes = []
        morphstring = u['morphology']['morphemes']

        if morphstring == None or morphstring == '':
            u['utterance']['warning'] = 'not glossed'
            return []

        morphstring = re.sub('(^|\\s)[\.\?!:\+\/]+(\\s|$)', '\\1\\2', morphstring) # utterance delimiters and codes
        morphstring = re.sub('(^|\\s)tag\|\\S+(\\s|$)', '\\1\\2', morphstring) # tags
        morphstring = re.sub('\\s+$', '', morphstring)
        # other clutter
        morphstring = re.sub('&', '.', morphstring) # joins glosses
        morphstring = re.sub('\+', '_', morphstring) # marks word number mismatches between orthography and morphology (but is less frequent than "_")
        morphstring = re.sub('([A-Z]\\S*):\\s+', '\\1', morphstring) # POS tags gone astray: join with following word
        morphstring = re.sub('([^\|]+)\|([^\|]+)\|', '\\1/\\2|', morphstring) # double POS tags: replace "|" by "/"
                        
        # split mor tier into words, reset counter to -1
        mwords = re.split('\\s+',morphstring)
        
        # go through words on gloss tier
        ic = itertools.count()
        length_morphology = len(mwords)
        while True:
            i = next(ic)
            if i >= length_morphology or i >= len(u['words']):
                break
            w = mwords[i]
            try:
                if u['words'][i]['warning'] == 'not glossed':
                    mwords.insert(i, '')
                    length_morphology += 1
                    continue
            except KeyError:
                pass

            if '_' in w:
                wmors = w.split('_')
                if '_'  in u['words'][i]['full_word_target']:
                    pass
                else:
                    for j in range(len(wmors)):
                        mwords.insert(i+j, wmors[j])
                        
            # colon:
            #   in POS tag -> . (= subcategory)
            #   after stem -> . (= non-concatenative morphology)
            #   in suffix -> . (= subgloss)
            # ==> keep for now, this should be done by postprocessing
            
            # split into POS tag and gloss
            if '|' in w:
                parts = w.partition('|')
                stem_pos = parts[0]
                gloss = parts[2]
            elif '/' in w:
                parts = w.partition('/')
                stem_pos = parts[0]
                gloss = parts[2]
            else:
                stem_pos = None
                gloss = w
        
            # morphemes per word
            word_mors = []
            # split into stem and possible suffixes; split suffix chain if exists
            check_stem = re.search('^([^\\-]+)(.*)$', gloss)
            (stem, suffix_string) = ('', '')
            if check_stem:
                stem = check_stem.group(1)
                suffix_string = check_stem.group(2)
        
                # add stem, gloss (unknown), and POS for stem to corpus dic
                mdic = {}
                mdic['segments_target'] = stem
                mdic['glosses_target'] = '???'
                mdic['pos_target'] = stem_pos
                word_mors.append(mdic)
        
            if suffix_string:
                # drop first hyphen in suffix string so split() doesn't produce empty elements
                suffix_string = suffix_string.lstrip("-")
                for suffix_gloss in suffix_string.split('-'):
                    mdic = {}
                    mdic['segments_target'] = '???'
                    mdic['glosses_target'] = suffix_gloss
                    mdic['pos_target'] = 'sfx'
                    word_mors.append(mdic)

            if word_mors != []:
                morphemes.append(word_mors)

        # EOF word loop
        
        # go through words <w> and insert glosses for repetitions and retracings (warning 'not glossed; repeat/search ahead')
        for i in range(0, len(u['words'])):
            
            if('warning' in u['words'][i].keys() and
                re.search('not glossed; (repeat|search ahead)', u['words'][i]['warning'])):
                
                # count up number of glossed words
                length_morphology += 1
                
                # (1) repetitions: get morphology from preceding word 
                if 'repeat' in  u['words'][i]['warning']:
                    if i != 0:
                        morphemes[i] = morphemes[i-1]
                
                # (2) retracings: get morphology from any matching word further ahead
                if 'search ahead' in u['words'][i]['warning']:
                    # go through all following <w> 
                    for j in range(i, len(u['words'])):
                        # corresponding target words: transfer morphology
                        if u['words'][j]['full_word_target'] == u['words'][i]['full_word_target']:
                            # transfer gloss from match to present word
                            morphemes[i] = morphemes[j]
                        # corresponding actual words: transfer morphology AND target word
                        elif u['words'][j]['full_word'] == u['words'][i]['full_word']:
                            # transfer gloss and target from match to present word
                            morphemes[i] = morphemes[j]
                            u['words'][i]['full_word_target'] = u['words'][j]['full_word_target']
                    
                # remove warning and delete key if empty
                # print(utterance_index, u['words'][i]['warning'])
                if 'warning' in u['words'][i].keys():
                    u['words'][i]['warning'] = re.sub(';?\\s*not glossed; (repeat|search ahead)', '', u['words'][i]['warning'])
                if u['words'][i]['warning'] == '':
                    del u['words'][i]['warning']

        # EOF glosses for repetitions/retracings 

        # check alignment with words that were found in <w>
        if length_morphology != len(u['words']):
            #print('alignment problem in ' + file_name + ', utterance ' + str(utterance_id) + ': general word tier <w> has ' 
            #    + str(corpus[text_id][utterance_index]['length_in_words']) + ' words vs ' + str(length_morphology) + ' in "mor" (= morphology)')
            u['utterance']['warning'] = 'broken alignment full_word : segments/glosses'

        if len(morphemes) == 0:
            u['utterance']['warning'] = 'not glossed'

        return morphemes

    # if there is no morphology, add warning to complete utterance
        
# EOF Turkish_KULLD

    def _get_timestamps(self, u):
        ts = u.find('.//media')
        if ts != None:
            return (ts.attrib.get('start'), ts.attrib.get('end'))
        else:
            return (None, None)

    def next_utterance(self):
        for u in self._get_utts():
            morph = self._morphology_inference(u)
            for w,ms in itertools.takewhile(lambda x: x[1] != None, 
                    itertools.zip_longest(u['words'], morph)):
                for m in ms:
                    try:
                        m['word_id_fk'] = w['word_id']                
                    except TypeError:
                        m = None
                        continue
            u['morphology'] = morph
            yield u['utterance'], u['words'], u['morphology']
