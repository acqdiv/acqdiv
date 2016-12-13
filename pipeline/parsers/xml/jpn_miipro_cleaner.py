# -*- coding: utf-8 -*-

import copy
import re
import sys
import itertools
import pdb

from lxml import etree
from pipeline.parsers.xml.xml_cleaner import XMLCleaner

class MiiProCleaner(XMLCleaner):

    def _get_timestamps(self, u):
        ts = u.find('.//media')
        if ts != None:
            return (ts.attrib.get('start'), ts.attrib.get('end'))
        else:
            return (None, None)

    def _process_morphology(self, u):

        full_words = u.findall('.//w')
        wlen = len(full_words)

        morphology = u.find("a[@type='extension'][@flavor='trn']")
        if morphology is not None:
            # remove punctuation and tags
            morphology.text = re.sub('(^|\\s)[\.\?!\+\/]+(\\s|$)', '\\1\\2', morphology.text)
            morphology.text = re.sub('(^|\\s)tag\|\\S+(?=\\s|$)', '\\1', morphology.text) # right context as lookahead to cover case of double tags 
            
            morphology.text = re.sub('\\s+$', '', morphology.text)
                            
            # split trn tier into words, reset counter
            words = re.split('\\s+', morphology.text)
            word_index = -1
            
            # go through words on gloss tier
            for w in words:
            
                # count up word index, extend list if necessary
                word_index, wlen = XMLCleaner.word_index_up(
                        full_words, wlen, word_index, u)

                    # some words in <w> have a warning "not glossed": this means there is no element on the morphology tier corresponding to the present <w>
                    # -> incremeent the <w> counter by one as long as the present morphological word is associated with the next <w>
                try:
                    while('warning' in full_words[word_index].attrib and
                        re.search('not glossed',full_words[word_index].attrib['warning'])):
                        word_index += 1
                except IndexError:
                    return
                                                        
                mword = etree.SubElement(full_words[word_index], 'mor')
                mword.text = w

            u.remove(morphology)

    def _morphology_inference(self, u):
        # go through words on gloss tier
        full_words = u.findall('.//w')
        word_index = -1
        for wd in full_words:

            word_index += 1

            if ('warning' in wd.attrib.keys() 
                    and wd.attrib['warning'] == 'not glossed'):
                word_index += 1
                continue

            mw = wd.find('mor')

            if mw is None:
                word_index += 1
                continue
        
            w = mw.text
            # morphemes per word
            prefix = ''
            check_pfx = re.search('^(.+#)', w)
            if check_pfx:
                prefix = check_pfx.group(1) 
                gloss = w.lstrip(prefix)
                prefix = prefix.replace('#', '')

                m = etree.SubElement(mw, 'm')
                m.attrib['segments_target'] = prefix
                m.attrib['glosses_target'] = '???'
                m.attrib['pos_target'] = 'pfx'

            stem_gloss = '???'
            check_stem_gloss = re.search('(.+)=(\S+)$', w)
            if check_stem_gloss:
                w = check_stem_gloss.group(1)
                stem_gloss = check_stem_gloss.group(2)
            
            # split into compound elements (if applicable)
            compound_elems = w.split('+')
            for i in range(0, len(compound_elems)):
                
                # split into POS tag and gloss; add '=' as separator to posterior compound elements
                parts = compound_elems[i].partition('|')
                stem_pos = parts[0]
                gloss = parts[2]
                if i>0: gloss = '=' + gloss
                
                # split into stem and possible suffixes; split suffix chain if exists
                check_stem = re.search('^([^\\-]+)(.*)$', gloss)
                (stem, suffix_string) = ('', '')
                if check_stem:
                    
                    stem = check_stem.group(1)
                    suffix_string = check_stem.group(2)
                    # Japanese MiiPro specialty: grammatical categories in suppletive forms are marked by '&' (e.g. da&POL = des); replace by '.'
                    stem = stem.replace('&','.')
                
                    # add stem, suffixes, and POS for all to corpus dic
                    m = etree.SubElement(mw, 'm')
                    m.attrib['segments_target'] = stem
                    m.attrib['glosses_target'] = stem_gloss
                    m.attrib['pos_target'] = stem_pos
                
                if suffix_string:
                    # drop first hyphen in suffix string so split() doesn't produce empty elements
                    suffix_string = suffix_string.lstrip("-")
                    for suffix_gloss in suffix_string.split('-'):
                        # count up morpheme index, extend list if necessary
                        
                        # most suffixes don't have form glosses in MiiPro, but sometimes blocks of the type IMP:te are found, in which case IMP is the suffix gloss and -te is the suffix form. Only exception is [A-Z]:contr, which is not a stem gloss but indicates contractions.
                        suffix_form = '???'
                        check_suffix = re.search('^([A-Z]+):(\w+)$', suffix_gloss)
                        if check_suffix and check_suffix.group(2) != 'contr':
                            suffix_gloss = check_suffix.group(1)
                            suffix_form = check_suffix.group(2)
                        
                        m = etree.SubElement(mw, 'm')
                        m.attrib['segments_target'] = suffix_form
                        m.attrib['glosses_target'] = suffix_gloss
                        m.attrib['pos_target'] = 'sfx'
                        
        # EOF word loop
            mw.text = ''
        
        # go through words <w> and insert glosses for repetitions and retracings (warning 'not glossed; repeat/search ahead')

        # EOF glosses for repetitions/retracings 

        # check alignment with words that were found in <w>
        # if there is no morphology, add warning to complete utterance


    # EOF Japanese_MiiPro
    

if __name__ == '__main__':

    from parsers import CorpusConfigParser as Ccp
    conf = Ccp()
    conf.read('ini/Japanese_MiiPro.ini')
    corpus = MiiProCleaner(conf, 'tests/corpora/Japanese_MiiPro/xml/Japanese_MiiPro.xml')

    corpus._debug_xml()

