# -*- coding: utf-8 -*-

import re
import sys
import itertools

from lxml import etree
from XMLParser import XMLParser

class CreeParser(XMLParser):

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
        return [{"full_word": w.text, "full_word_target": w.attrib['target'],
            "utterance_id_fk": u.attrib.get('uID'), 
            "word_id": (u.attrib.get('uID') + 'w' + str(i))} 
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

        morph = u['morphology']

        if morph['morphemes'] != None:
            mortext = morph['morphemes']
            mortext = re.sub('\\s+(&gt;|>)\\s+', '>', mortext)
            # remove square brackets at edges of any of these tiers, they are semantically redundant
            mortext = re.sub('^\[|\]$', '', mortext)
            # replace untranscribed and/or unglossed words by standard formalisms
            mortext = re.sub('#|%%%|\*|(?<=\\s)\?(?=\\s)', '???', mortext)
            mortext = re.sub('[\(\)]', '', mortext)
            mortext = re.sub('zéro', 'Ø', mortext)
            morph['morphemes'] = mortext
        else:
            morph['morphemes'] = ''

        if morph['gloss_raw'] != None:
            gltext = morph['gloss_raw']
            gltext = re.sub('\\s+(&gt;|>)\\s+', '>', gltext)
            # remove square brackets at edges of any of these tiers, they are semantically redundant
            gltext = re.sub('^\[|\]$', '', gltext)
            # replace untranscribed and/or unglossed words by standard formalisms
            gltext = re.sub('#|%%%|\*|(?<=\\s)\?(?=\\s)', '???', gltext)
            gltext = re.sub('zéro', 'Ø', gltext)
            morph['gloss_raw'] = gltext
        else:
            morph['gloss_raw'] = ''

        if morph['pos_raw'] != None:
            postext = morph['pos_raw']
            postext = re.sub('\\s+(&gt;|>)\\s+', '>', postext)
            # remove square brackets at edges of any of these tiers, they are semantically redundant
            postext = re.sub('^\[|\]$', '', postext)
            # replace untranscribed and/or unglossed words by standard formalisms
            postext = re.sub('#|%%%|\*|(?<=\\s)\?(?=\\s)', '???', postext)
            # delete brackets in "mortyp" and uppercase content to emphasise its abstract nature
            postext = re.sub('\(([^\)]+)\)', '\\1'.upper(), postext)
            postext = re.sub('zéro', 'Ø', postext)
            morph['pos_raw'] = postext
        else:
            morph['pos_raw'] = ''

        tiers = ['morphemes', 'gloss_raw', 'pos_raw']

        if morph['morphemes'] == '' and morph['gloss_raw'
                ] == '' and morph['pos_raw'] == '':
            u['utterance']['warning'] = "not glossed"
            return morph

        for tier in tiers:
            
            text = morph[tier]

            if text != None:

                words = re.split('\\s+', text)

                if len(words) != len(u['words']):
                    # log error
                    #print("Alignment error! Oh no!", file=sys.stderr)
                    if u['utterance']['warning'] != None:
                        u['utterance']['warning'] += ("broken alignment: " 
                            "{bad_tier}".format(bad_tier=tier))
                    else:
                        u['utterance']['warning'] = ("broken alignment: "
                            "{bad_tier}".format(bad_tier=tier))

                    morph[tier] = []

                else:

                    mlist = []
                    for mw in words:
                        ms = mw.split('~')
                        mlist.append(ms)
                    morph[tier] = mlist

            else:
                morph[tier] = ['']

        #out = [[{'morphemes':m, 'gloss_raw':g, 'pos_raw':p} for m,g,p in mt]
        #        for mt in filter(lambda x: x != None, 
        #            itertools.zip_longest(morph['morphemes'], 
        #            morph['gloss_raw'], morph['pos_raw']))]

        if u['utterance']['warning'] == (
        "broken alignment: morphemesbroken alignment: "
        "gloss_rawbroken alignment: pos_raw"):
            u['utterance']['warning'] = "not glossed"

        out = []
        for mt,gt,pt in itertools.zip_longest(morph['morphemes'],
                morph['gloss_raw'], morph['pos_raw'], fillvalue=""):
            try:
                out.append([{'morpheme':m, 'gloss_raw':g, 'pos_raw':p} for m,g,p in 
                        itertools.zip_longest(mt,gt,pt)])
            except TypeError:
                print(mt,gt,pt)
                out.append({'morphemes':None, 'gloss_raw':None, 'pos_raw':None})

        return out

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
