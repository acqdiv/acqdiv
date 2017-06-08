# -*- coding: utf-8 -*-

import itertools
import pdb
import re
import sys

from lxml import etree
from .xml_cleaner import XMLCleaner

class CreeCleaner(XMLCleaner):

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
                # Cree: where the orthography tier is missing <w> is not 
                # empty but contains 'missingortho' -> remove this
                wt.text = re.sub('missingortho', '', wt.text)
                # Cree: replace "zéro" (= zero morpheme) by more standard "Ø"
                wt.text = re.sub('zéro', 'Ø', wt.text)
                # Sometimes words may be partially untranscribed 
                # (-xxx, xxx-, -xxx-) - transform this, too
                wt.text = re.sub('\-?xxx\-?', '???', wt.text)
                # only in Cree: morpheme boundaries in <w> are indicated by '_'
                # -> remove these, segments are also given in the morphology 
                # tiers. Other corpora can have '_' in <w>, too, but there it's
                # meaningful (e.g. for concatenating the parts of a book title
                # treated as a single word)
                wt.text = re.sub('_', '', wt.text)

            if 'untranscribed' in w.attrib:
                wt.text = '???'

    def _remove_junk(self, u):
        pg = u.find('pg')
        actpho = pg.find('actual')
        tarpho = pg.find('model')

        if actpho is not None:
            pg.remove(actpho)
        if tarpho is not None:
            pg.remove(tarpho)

    def _process_morphology(self, u):
        for morph_tier in ('tarmor', 'actmor', 'mormea', 'mortyp'):
            tier = u.find("a[@type='extension'][@flavor='" + morph_tier + "']")
            if tier is not None:

                # edit tier syntax
                # first remove spaces within glosses so that only word boundary markers remain
                tier.text = re.sub('\\s+(&gt;|>)\\s+', '>', tier.text)
                # remove square brackets at edges of any of these tiers, they are semantically redundant
                tier.text = re.sub('^\[|\]$', '', tier.text)
                # replace untranscribed and/or unglossed words by standard formalisms
                tier.text = re.sub('#|%%%|\*|(?<=\\s)\?(?=\\s)', '???', tier.text)
                # delete brackets in "mortyp" and uppercase content to emphasise its abstract nature
                if morph_tier == 'mortyp':
                    tier.text = re.sub('\(([^\)]+)\)', '\\1'.upper(), tier.text)
                # delete brackets in "tarmor" and "actmor"
                if morph_tier == 'tarmor' or morph_tier == 'actmor':
                    tier.text = re.sub('[\(\)]', '', tier.text)
                # replace "zéro" (= zero morpheme) by more standard "Ø"
                tier.text = re.sub('zéro', 'Ø', tier.text)

                # split into words
                words = re.split('\\s+', tier.text)
                full_words = u.findall('.//w')
                wlen = len(full_words)
                word_index = -1

                for w in words:

                    word_index, wlen = XMLCleaner.word_index_up(
                            full_words, wlen, word_index, u)

                    if full_words[word_index].find('tmor') is None:
                        mor = etree.SubElement(full_words[word_index], 'tmor')
                    else:
                        mor = full_words[word_index].find('tmor')
                    mtier = etree.SubElement(mor, morph_tier)
                    mtier.text = words[word_index]

                u.remove(tier)

    def _morphology_inference(self, u):

        full_words = u.findall('.//w')
        # split words into morphemes, add to temporary Vividict
        word_index = 0
        for wd in full_words:
            temp = wd.find('tmor')
            if temp is not None:
                tiers = temp.getchildren()
                mword = etree.SubElement(wd, 'mor')
                for tier in tiers:
                    morpheme_index = 0
                    morphemes = re.split('~', tier.text)
                    for m in morphemes:
                        if morpheme_index >= len(mword):
                            mor = etree.SubElement(mword, 'm')
                        else:
                            mor = mword[morpheme_index]

                        mor.attrib[self.cfg['correspondences'][tier.tag]] = m
                        morpheme_index += 1

                wd.remove(temp)
                word_index += 1
            else:
                XMLCleaner.creadd(wd.attrib, 'warning', 'not glossed')
                word_index += 1
                continue

        mortyp_t = self.cfg['correspondences']['mortyp']
        mormea_t = self.cfg['correspondences']['mormea']
        for wd in full_words:

            ms = wd.find('mor')
            if ms is not None:
                for w in ms:

                    # some corrections where the Cree tier names don't match our target tiers exactly
                    if (mortyp_t in w.attrib and w.attrib[mortyp_t] == 'IMP'
                            and mormea_t in w.attrib):
                        w.attrib[mormea_t] += '.' + w_attrib[mortyp_t]
                        w.attrib[mortyp_t] = 'sfx'
                    # English words are glossed as "Eng" -> replace this by the word itself (e.g. "two", gloss "Eng" -> "two", gloss "two")
                    if mormea_t in w.attrib and w.attrib[mormea_t] == 'Eng':
                        wdl = etree.SubElement(wd, 'language')
                        wdl.text = 'English'
                        w.attrib['language'] = 'English'
                        w.attrib[mormea_t] = wd.find('actual').text
                    else:
                        wdl = etree.SubElement(wd, 'language')
                        wdl.text = 'Cree'
                        w.attrib['language'] = 'Cree'
                    # check for "?" attached to gloss; replace by warning that gloss is insecure
                    if mormea_t is w.attrib and w.attrib[mormea_t].endswith('?'):
                        w.attrib[mormea_t] = w.attrib[mormea_t][:-1]
                        XMLCleaner.creadd(ms.attrib, 'warning', 'gloss insecure for tier ' + mormea_t)
         # EOF word loop
     # EOF Cree


if __name__ == '__main__':
    from parsers import CorpusConfigParser as Ccp
    conf = Ccp()
    conf.read('ini/Cree.ini')
    corpus = CreeCleaner(conf, 'tests/corpora/Cree/xml/Cree.xml')

    corpus._debug_xml()

