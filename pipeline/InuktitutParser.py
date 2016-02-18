# -*- coding: utf-8 -*-

import re
import sys
import itertools

from lxml import etree
from XMLParser import XMLParser

class InuktitutParser(XMLParser):
    def next_utterance(self):
        for u in self._get_utts():
            # morph = self._morphology_inference(u)
            """
            for w, ms in itertools.takewhile(lambda x: x[1] != None,
                    itertools.zip_longest(u['words'], morph)):
                for m in ms:
                    try:
                        m['word_id_fk'] = w['word_id']
                    except TypeError:
                        m = None
                        continue
            """
            # u['morphology'] = morph
            # u['morphology'] = None
            yield u['utterance'], u['words'], u['morphology']
    """
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
            u['utterance']['warnings'] = "not glossed"
            return morph

        for tier in tiers:

            text = morph[tier]

            if text != None:

                words = re.split('\\s+', text)

                if len(words) != len(u['words']):
                    # log error
                    #print("Alignment error! Oh no!", file=sys.stderr)
                    if u['utterance']['warnings'] != None:
                        u['utterance']['warnings'] += ("broken alignment: "
                            "{bad_tier}".format(bad_tier=tier))
                    else:
                        u['utterance']['warnings'] = ("broken alignment: "
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

        if u['utterance']['warnings'] == (
        "broken alignment: morphemesbroken alignment: "
        "gloss_rawbroken alignment: pos_raw"):
            u['utterance']['warnings'] = "not glossed"

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
        """