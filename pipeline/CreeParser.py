# -*- coding: utf-8 -*-

import re
import sys
import itertools

from lxml import etree
from XMLParser import XMLParser

class CreeParser(XMLParser):

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
                # Cree: where the orthography tier is missing <w> is not 
                # empty but contains 'missingortho' -> remove this
                w.text = re.sub('missingortho', '', w.text)
                # Cree: replace "zéro" (= zero morpheme) by more standard "Ø"
                w.text = re.sub('zéro', 'Ø', w.text)
                # Sometimes words may be partially untranscribed 
                # (-xxx, xxx-, -xxx-) - transform this, too
                w.text = re.sub('\-?xxx\-?', '???', w.text)
                # only in Cree: morpheme boundaries in <w> are indicated by '_'
                # -> remove these, segments are also given in the morphology 
                # tiers. Other corpora can have '_' in <w>, too, but there it's
                # meaningful (e.g. for concatenating the parts of a book title
                # treated as a single word)
                w.text = re.sub('_', '', w.text)
            if 'untranscribed' in w.attrib:
                w.text = '???'
        return words

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

        if morph['gloss_raw'] != None:
            gltext = morph['gloss_raw']
            gltext = re.sub('\\s+(&gt;|>)\\s+', '>', gltext)
            # remove square brackets at edges of any of these tiers, they are semantically redundant
            gltext = re.sub('^\[|\]$', '', gltext)
            # replace untranscribed and/or unglossed words by standard formalisms
            gltext = re.sub('#|%%%|\*|(?<=\\s)\?(?=\\s)', '???', gltext)
            gltext = re.sub('zéro', 'Ø', gltext)
            morph['gloss_raw'] = gltext

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

        tiers = ['morphemes', 'gloss_raw', 'pos_raw']

        if morph['morphemes'] == None and morph['gloss_raw'
                ] == None and morph['pos_raw'] == None:
            XMLParser.creadd(u['utterance'], 'warning', "not glossed")

        for tier in tiers:
            
            text = morph[tier]

            if text != None:

                words = re.split('\\s+', text)

                if len(words) != len(u['words']):
                    # log error
                    #print("Alignment error! Oh no!", file=sys.stderr)
                    XMLParser.creadd(u['utterance'], 'warning', 
                            "broken alignment: {bad_tier}".format(bad_tier=tier))


                mlist = []
                for mw in words:
                    ms = mw.split('~')
                    mlist.append(ms)
                morph[tier] = mlist

            else:
                morph[tier] = []

        #out = [[{'morphemes':m, 'gloss_raw':g, 'pos_raw':p} for m,g,p in mt]
        #        for mt in filter(lambda x: x != None, 
        #            itertools.zip_longest(morph['morphemes'], 
        #            morph['gloss_raw'], morph['pos_raw']))]

        if u['utterance']['warning'] == (
        "broken alignment: morphemes; broken alignment: "
        "gloss_raw; broken alignment: pos_raw"):
            u['utterance']['warning'] = "not glossed"

        out = []
        for mt,gt,pt in itertools.zip_longest(morph['morphemes'],
                morph['gloss_raw'], morph['pos_raw'], fillvalue=[]):
            try:
                out.append([{'morpheme':m, 'gloss_raw':g, 'pos_raw':p} for m,g,p in 
                        itertools.zip_longest(mt, gt, pt, fillvalue=None)])
            except TypeError:
                print(mt,gt,pt)
                out.append([{'morphemes':None, 'gloss_raw':None, 'pos_raw':None}])

        return out

