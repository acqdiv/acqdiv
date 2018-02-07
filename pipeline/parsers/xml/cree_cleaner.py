# -*- coding: utf-8 -*-

import re

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
        """Clean morpheme words and re-structure XML of utterance.

        Restructure of XML:
            - new element <tmor> under <w>
            - morpheme data in <a> inserted under <tmor>
            - <a>'s with morpheme data are deleted

        Example output of <w>:
            <w>
                <actual>...</actual>
                <target>...</target>
                <tmor>
                    <tarmor>...</tarmor>
                    <actmor>...</actmor>
                    <mormea>...</mormea>
                    <mortyp>...</mortyp>
                </tmor>
            </w>
        """
        # Go through all morpheme tiers
        for morph_tier in ('tarmor', 'actmor', 'mormea', 'mortyp'):
            # Get the element of this morpheme tier
            tier = u.find("a[@type='extension'][@flavor='" + morph_tier + "']")

            if tier is not None:

                # Cleaning
                # first remove spaces within glosses
                # so that only word boundary markers remain
                tier.text = re.sub('\\s+(&gt;|>)\\s+', '>', tier.text)
                # remove square brackets at edges of any of these tiers
                # they are semantically redundant
                tier.text = re.sub('^\[|\]$', '', tier.text)
                # replace untranscribed and/or unglossed words
                # by standard formalisms
                tier.text = re.sub(
                    '#|%%%|\*|(?<=\\s)\?(?=\\s)', '???', tier.text)
                # delete brackets in "mortyp" and uppercase content
                # to emphasise its abstract nature
                if morph_tier == 'mortyp':
                    tier.text = re.sub(
                        '\(([^\)]+)\)', '\\1'.upper(), tier.text)
                # delete brackets in "tarmor" and "actmor"
                if morph_tier == 'tarmor' or morph_tier == 'actmor':
                    tier.text = re.sub('[\(\)]', '', tier.text)
                # replace "zéro" (= zero morpheme) by more standard "Ø"
                tier.text = re.sub('zéro', 'Ø', tier.text)

                # split into m-words
                words = re.split('\\s+', tier.text)
                # get w-words
                full_words = u.findall('.//w')
                # get number of w-words
                wlen = len(full_words)
                # current position of w-word
                word_index = -1

                # go through all m-words
                for w in words:

                    # add dummy word to w-words if < no. m-words
                    # get updated word position and no. w-words
                    word_index, wlen = XMLCleaner.word_index_up(
                            full_words, wlen, word_index, u)

                    # check if <tmor>-element is already inserted under the
                    # the corresponding <w>-element
                    if full_words[word_index].find('tmor') is None:
                        mor = etree.SubElement(full_words[word_index], 'tmor')
                    else:
                        mor = full_words[word_index].find('tmor')

                    # insert morpheme tier element under <tmor>-element
                    mtier = etree.SubElement(mor, morph_tier)
                    # set text with content of morpheme tier
                    mtier.text = words[word_index]

                # remove <a>-elements with morpheme data
                u.remove(tier)

    def _morphology_inference(self, u):
        # get all <w> elements
        full_words = u.findall('.//w')
        # position of word in utterance
        word_index = 0
        # go through all <w> elements
        for wd in full_words:
            # get the <tmor> element
            temp = wd.find('tmor')
            # check if it exists
            if temp is not None:
                # get all morpheme elements which are under <tmor>
                tiers = temp.getchildren()
                # create the element <mor> under the <tmor> element
                mword = etree.SubElement(wd, 'mor')
                # go through morpheme elements
                for tier in tiers:
                    # position of a morpheme within word
                    morpheme_index = 0
                    # split into morphemes at '~'
                    morphemes = re.split('~', tier.text)
                    # go through all morphemes
                    for m in morphemes:
                        # create as many <m> elements as there are morphemes
                        # (taking the morpheme tier with most morphemes)
                        if morpheme_index >= len(mword):
                            # create the <m> under the <mor> element
                            # TODO: rename this variable to 'm_element'
                            mor = etree.SubElement(mword, 'm')
                        else:
                            # get the <m> element
                            mor = mword[morpheme_index]

                        # get morpheme tier name and look up the standard name
                        # in the ini and add this name and the morpheme value
                        # as an attribute of the <m> element
                        mor.attrib[self.cfg['correspondences'][tier.tag]] = m
                        morpheme_index += 1

                # remove the <tmor> element
                wd.remove(temp)
                word_index += 1
            else:
                # create a warning if <tmor> element does not exist
                XMLCleaner.creadd(wd.attrib, 'warning', 'not glossed')
                word_index += 1
                continue

        # get standard name of morpheme tiers mortyp and mormea in ini
        mortyp_t = self.cfg['correspondences']['mortyp']
        mormea_t = self.cfg['correspondences']['mormea']
        # go through <w> elements
        for wd in full_words:
            # get <mor> element
            ms = wd.find('mor')
            # check if it exists
            if ms is not None:
                # go through <m> elements
                for w in ms:
                    # some corrections where the Cree tier names don't match
                    # our target tiers exactly
                    if (mortyp_t in w.attrib and w.attrib[mortyp_t] == 'IMP'
                            and mormea_t in w.attrib):
                        # concatenate '.IMP' to mormea
                        w.attrib[mormea_t] += '.' + w.attrib[mortyp_t]
                        # replace 'IMP' by 'sfx'
                        w.attrib[mortyp_t] = 'sfx'

                    # English words are glossed as "Eng"
                    # replace this by the word itself
                    # (e.g. "two", gloss "Eng" -> "two", gloss "two")
                    if mormea_t in w.attrib and w.attrib[mormea_t] == 'Eng':
                        # create <language> under <w> element
                        wdl = etree.SubElement(wd, 'language')
                        # set text of this element to 'English'
                        wdl.text = 'English'
                        # create an attribute 'language' with value 'English'
                        # in the <m> element
                        w.attrib['language'] = 'English'
                        # set mormea to the actual word form
                        w.attrib[mormea_t] = wd.find('actual').text
                    else:
                        # create language <language> element with text 'Cree'
                        # under <w> element
                        wdl = etree.SubElement(wd, 'language')
                        wdl.text = 'Cree'
                        # create an attribute 'language' with value 'Cree'
                        # in the <m> element
                        w.attrib['language'] = 'Cree'

                    # check for "?" attached to gloss
                    if (mormea_t in w.attrib
                            and w.attrib[mormea_t].endswith('?')):
                        # delete '?'
                        w.attrib[mormea_t] = w.attrib[mormea_t][:-1]
                        # create warning that gloss is insecure
                        XMLCleaner.creadd(
                            ms.attrib, 'warning',
                            'gloss insecure for tier ' + mormea_t)


if __name__ == '__main__':
    from parsers import CorpusConfigParser as Ccp
    conf = Ccp()
    conf.read('ini/Cree.ini')
    corpus = CreeCleaner(conf, 'tests/corpora/Cree/xml/Cree.xml')

    corpus._debug_xml()
