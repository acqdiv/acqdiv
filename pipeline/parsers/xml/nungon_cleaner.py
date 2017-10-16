# -*- coding: utf-8 -*-

import re
import itertools

from lxml import etree
from .xml_cleaner import XMLCleaner


class NungonCleaner(XMLCleaner):

    def _process_morphology(self, u):
        """Clean segment and gloss words."""

        full_words = u.findall('.//w')
        wlen = len(full_words)
        segment_words = None
        gloss_words = None

        # process segments
        # try out which segment attribute is used (target gloss/gls)
        segment_tier = u.find("a[@type='target gloss']")
        if segment_tier is None:
            segment_tier = u.find("a[@flavor='gls']")
        if segment_tier is not None:
            word_index = -1

            # remove everything with brackets, e.g. '[cries]'
            segment_tier.text = re.sub(
                    r'\[.*?\]', '', segment_tier.text)
            # strip trailing/leading whitespaces
            segment_tier.text = segment_tier.text.strip(' ')
            # strip braces
            segment_tier.text = segment_tier.text.strip('(').strip(')')
            # strip punctuation (.?)
            segment_tier.text = re.sub(r'\.$|\?\.?$', '', segment_tier.text)

            # create a list of segments splitting at whitespaces and =
            segment_words = re.split(r'\s+|=', segment_tier.text)

            for w in segment_words:

                # ignore anything starting with '&=', e.g. '&amp;=toron'
                if w.startswith('&') or w == '+//':
                    continue

                # set unknown segments to 'xxx'
                if w == '?':
                    w = 'xxx'

                # check for mismatches in the number of <w>'s and segment words
                word_index, wlen = XMLCleaner.word_index_up(
                                        full_words, wlen, word_index, u)
                mor = etree.SubElement(full_words[word_index], 'mor')
                seg = etree.SubElement(mor, 'seg')
                seg.text = w

            u.remove(segment_tier)

        # Glosses and POS
        gloss_tier = u.find("a[@flavor='cod']")
        if gloss_tier is not None:
            word_index = -1

            # remove everything with brackets, e.g. '[cries]'
            gloss_tier.text = re.sub(
                    r'\[.*?\]', '', gloss_tier.text)
            # strip trailing/leading whitespaces and trailing dots
            gloss_tier.text = gloss_tier.text.strip(" ").rstrip(".")

            # create a list of gloss-words splitting at whitespaces and =
            gloss_words = re.split(r'\s+|=', gloss_tier.text)

            # go through words
            for w in gloss_words:
                # ignore anything starting with '&=', e.g. '&amp;=toron'
                if w.startswith('&'):
                    continue

                # strip leading and trailing #, e.g. 'dep#'
                w = w.strip('#')
                # only allow three xxx's
                w = re.sub(r'x{4,}', 'xxx', w)
                # set ambiguous glosses (with '#' as a separator) to 'xxx'
                w = re.sub(r'\S+#\S+', 'xxx', w)

                # check for mismatches in the number of <w>'s and gloss words
                word_index, wlen = XMLCleaner.word_index_up(
                                            full_words, wlen, word_index, u)
                mor = full_words[word_index].find('mor')
                if mor is None:
                    mor = etree.SubElement(full_words[word_index], 'mor')
                gl = etree.SubElement(mor, 'gl')
                gl.text = w

            u.remove(gloss_tier)

        # check alignment between segments and glosses on word level
        if segment_words is not None and gloss_words is not None:
            if len(gloss_words) != len(segment_words):
                self.creadd(u.attrib, 'warnings', 'broken alignment '
                            'segments_target : glosses_target')

    def _morphology_inference(self, u):
        """Clean and infer segment, gloss and pos on morpheme level."""
        for fw in u.findall('.//w'):
            mor = fw.find('mor')
            if mor is None:
                continue

            # get segments and glosses of a word
            seg = XMLCleaner.find_text(mor, 'seg')
            gl = XMLCleaner.find_text(mor, 'gl')

            # create list of segments/glosses splitting at '-'/'='
            segments = []
            glosses = []
            if seg is not None:
                segments = re.split(r'\-', seg)
            if gl is not None:
                glosses = re.split(r'\-', gl)

            # check alignment between segments and glosses on morpheme level
            if len(glosses) != len(segments):
                XMLCleaner.creadd(
                        fw.attrib, 'warnings',
                        'broken alignment segments_target : glosses_target')

            # iter glosses (pos+gloss) and segments
            # in case of mismatch -> empty string
            passed_stem = False
            ms = itertools.zip_longest(glosses, segments, fillvalue='')
            for gloss, segment in ms:
                # replace '+' by '.' in gloss, e.g. '1sg+ben'
                gloss = gloss.replace('+', '.')
                # replace '%'/'&' by '^' as pos-gloss separator, e.g. 'd%prox'
                gloss = gloss.replace('%', '^')
                gloss = gloss.replace('&', '^')
                # replace '.' by '/' between numbers in gloss, e.g.'2.3pl'
                gloss = gloss.replace('/', '.')
                segment = segment.strip('?')

                # TODO: proper names are coded in POS
                # e.g. tpn -> noun + Tok Pisin

                # set pos and gloss
                # as long as stem is not passed, treat it as prefix
                # as soon as stem is passed, treat it as suffix
                pos = ''
                stem_match = re.search(r'([^-]+)\^([^-]+)', gloss)
                if stem_match:
                    passed_stem = True
                    pos = stem_match.group(1)
                    gloss = stem_match.group(2)
                else:
                    # TODO: stand-alone morphemes without explicit pos?
                    if len(glosses) == 1:
                        pos = gloss
                    else:
                        if not passed_stem:
                            pos = 'pfx'
                        else:
                            pos = 'sfx'

                # add under 'mor' as attributes in 'm'
                m = etree.SubElement(mor, 'm')
                m.attrib['glosses_target'] = gloss
                m.attrib['pos_target'] = pos
                m.attrib['segments_target'] = segment

            seg_n = mor.find('seg')
            gl_n = mor.find('gl')
            if seg_n is not None:
                mor.remove(seg_n)
            if gl_n is not None:
                mor.remove(gl_n)


if __name__ == "__main__":
    from parsers import CorpusConfigParser as Ccp
    conf = Ccp()
    conf.read('ini/Nungon.ini')
    corpus = NungonCleaner(conf, 'tests/corpora/Nungon/xml/Nungon.xml')
    corpus._debug_xml()
