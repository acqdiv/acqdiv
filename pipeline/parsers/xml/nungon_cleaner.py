# -*- coding: utf-8 -*-

import re
import itertools

from lxml import etree
from .xml_cleaner import XMLCleaner


class NungonCleaner(XMLCleaner):

    def _process_morphology(self, u):

        full_words = u.findall('.//w')
        wlen = len(full_words)

        segment_tier = u.find("a[@type='target gloss']")
        if segment_tier is None:
            segment_tier = u.find("a[@flavor='gls']")

        if segment_tier is not None:
            word_index = -1
            # split words at whitespaces
            segment_words = re.split('\\s+', segment_tier.text)

            for w in segment_words:
                # TODO: not attested yet
                if re.search('^(\(.*\)|[\.\?])$', w):
                    continue
                else:
                    # TODO: e.g. (naedi ma muuno)?
                    w = re.sub('[\(\)]', '', w)

                word_index, wlen = XMLCleaner.word_index_up(
                        full_words, wlen, word_index, u)

                mor = etree.SubElement(full_words[word_index], 'mor')
                seg = etree.SubElement(mor, 'seg')
                seg.text = w

            u.remove(segment_tier)

        # Glosses and POS
        gloss_tier = u.find("a[@flavor='cod']")
        if gloss_tier is not None:
            # set word index for inspecting temporary dict
            word_index = 0

            # the remaining spaces indicate word boundaries -> split
            gloss_words = re.split('\\s+', gloss_tier.text)

            # check alignment between segments and glosses on word level
            if len(gloss_words) != len(segment_words):
                self.creadd(u.attrib, 'warnings', 'broken alignment '
                            'segments_target : glosses_target')

            # reset word index for writing to corpus dict
            word_index = -1

            # go through words
            for w in gloss_words:

                # ignore punctuation in the segment/gloss tiers;
                # this shouldn't be counted as morphological words
                # TODO: !. not attested yet
                if re.search('^[.!\?]$', w):
                    continue

                # count up word index, extend list if necessary
                word_index += 1

                mor = full_words[word_index].find('mor')
                if mor is None:
                    mor = etree.SubElement(full_words[word_index], 'mor')
                gl = etree.SubElement(mor, 'gl')
                gl.text = w

            u.remove(gloss_tier)

    def _morphology_inference(self, u):
        full_words = u.findall('.//w')
        for fw in full_words:
            mor = fw.find('mor')
            if mor is None:
                continue
            else:
                seg = XMLCleaner.find_text(mor, 'seg')
                gl = XMLCleaner.find_text(mor, 'gl')

            # split at '-'/'=' into morphemes
            # do not split anything within square brackets
            segments = re.split(r'-|(?<!\&)=', seg) if seg is not None else []
            glosses = re.split(r'-|(?<!\&)=', gl) if gl is not None else []

            # check alignment between segments and glosses on morpheme level
            if len(glosses) != len(segments):
                XMLCleaner.creadd(
                        fw.attrib, 'warnings',
                        'broken alignment segments_target : glosses_target')

            # iter glosses and segments
            # in case of mismatch -> empty string
            passed_stem = False
            ms = itertools.zip_longest(glosses, segments, fillvalue='')
            for gloss, segment in ms:
                # TODO: handling of proper names?
                # set pos and gloss
                # as long as stem is not passed, treat it as prefix
                # as soon as stem is passed, treat it as suffix
                pos = ''
                stem_match = re.search(r'([^-=]+)\^([^-=]+)', gloss)
                if stem_match:
                    passed_stem = True
                    pos = stem_match.group(1)
                    gloss = stem_match.group(2)
                else:
                    # TODO: stand-alone morphemes without explicit pos?
                    # TODO: handling of anything within square brackets
                    if len(glosses) == 1:
                        pos = gloss
                    else:
                        # replace '_' by '.' in glosses
                        gloss = gloss.replace('_', '.')

                        if not passed_stem:
                            pos = 'pfx'
                        else:
                            pos = 'sfx'

                m = etree.SubElement(mor, 'm')
                # now put together segment, gloss, and POS
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
