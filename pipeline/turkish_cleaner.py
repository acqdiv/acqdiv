# -*- coding: utf-8 -*-

import copy
import re
import sys
import itertools
import pdb

from lxml import etree
from xml_parser import XMLCleaner

class TurkishCleaner(XMLCleaner):

    def _get_timestamps(self, u):
        ts = u.find('.//media')
        if ts != None:
            return (ts.attrib.get('start'), ts.attrib.get('end'))
        else:
            return (None, None)

    def _clean_fragments_and_omissions(self, words):
        for w in words:
            if 'type' in w.attrib:
                if 'type' == 'omission':
                    w = None
                    continue
                elif 'type' == 'fragment':
                    w.find('target').text = '???'
                    XMLCleaner.creadd(w.attrib, 'warning', 'not glossed')
                    continue
            if 'formType' in w.attrib and (w.attrib['formType'] 
                    in ['interjection', 'onomatopoeia', 'family-specific']):
                w.find('target').text = '???'
                XMLCleaner.creadd(w.attrib, 'warning', 'not glossed')
                continue

    def _process_morphology(self, u):

        full_words = u.findall('.//w')

        morphology = u.find("a[@type='extension'][@flavor='mor']")
        if morphology is not None:
            
            # remove punctuation and tags
            morphology.text = re.sub('(^|\\s)[\.\?!:\+\/]+(\\s|$)', '\\1\\2', morphology.text) # utterance delimiters and codes
            morphology.text = re.sub('(^|\\s)tag\|\\S+(\\s|$)', '\\1\\2', morphology.text) # tags
            morphology.text = re.sub('\\s+$', '', morphology.text)
            # other clutter
            morphology.text = re.sub('&amp;', '.', morphology.text) # joins glosses
            morphology.text = re.sub('\+', '_', morphology.text) # marks word number mismatches between orthography and morphology (but is less frequent than "_")
            morphology.text = re.sub('([A-Z]\\S*):\\s+', '\\1', morphology.text) # POS tags gone astray: join with following word
            morphology.text = re.sub('(\S+?)\|(\S+?)\|', '\\1/\\2|', morphology.text) # double POS tags: replace "|" by "/"
                            
            # split mor tier into words, reset counter to -1
            words = re.split('\\s+',morphology.text)
            word_index = -1
            
            # go through words on gloss tier
            for w in words:
                
                # count up word index, extend list if necessary
                word_index += 1

                # some words in <w> have a warning "not glossed": this means there is no element on the morphology tier corresponding to the present <w>
                # -> incremeent the <w> counter by one as long as the present morphological word is associated with the next <w>
                while('warning' in full_words[word_index].attrib and
                    re.search('not glossed',full_words[word_index].attrib['warning'])):
                    word_index += 1
                                                        
                # full_words[word_index]['morphemes'] is a list of morphemes; initial index is -1
                
                # when a word contains "_", it may code a single or two words. The following cases exist:

                # 1. shared tag+suffixes (PRO:INDEF|bir_şey) -> keep mor
                #   1.1 _ or + in <w> -> do nothing. 0 cases.
                #   1.2 two <w> -> fuse orth by "+". ~900 cases.
                # 2. separate tags+suffixes (V|N|tamir_V|et-IPFV-PL) -> split mor
                #   2.1 _ or + in <w> -> split orth, too. ~40 cases in corpus.
                #   2.2 two <w> -> keep orth. 0 cases.
                # only pervasive case is 1.2 -> deal with this, ignore the rest

                # check for "_" in morphological word ("+" is also possible but has been replaced by "_" further above)
                complex_mor = re.search('(\S+)_(\S+)', w)
                if complex_mor:
                    (mor_w1,mor_w2) = (complex_mor.group(1),complex_mor.group(2))
                    
                    # sometimes the part after the "_" has its own POS tag and/or suffixes. Linguistically it would be better to treat these
                    # cases as two words, but that would require further messing with <w>, so for the time being we remove the additional 
                    # POS tags and treat the whole thing as one word
                    # Note: there is a handful of cases (~10) where the mor word consists of three words. These are presently ignored (i.e. treated as if they were two words, e.g. Tom_ve_Jerry -> Tom_ve, Jerry).                        
                    if re.search('\|', mor_w2) or (re.search('\-', mor_w1) and re.search('\-', mor_w2)):
                        mor_w2 = re.sub('.*\|', '', mor_w2)
                        w = mor_w1 + '-' + mor_w2
                    
                    # next check in the orthography if there is a corresponding full word target and a following word
                    if (full_words[word_index].find('target').text
                            and len(full_words) > word_index+1
                            and full_words[word_index+1].find('target').text):
                        # finally check orthography of full_word_target for "_" or "+"
                        complex_orth = re.search('[_\+]', 
                                full_words[word_index].find('target').text)
                        if not complex_orth:
                            first = full_words[word_index]
                            second = full_words[word_index+1]

                            first_text = first.find('actual').text
                            second_text = second.find('actual').text

                            first_target = first.find('target').text
                            second_target = second.find('target').text

                            first_text = (first_text + '_' + second_text)
                            first_target = (first_target + '_' + second_target)
                            second.getparent().remove(second)

                mword = etree.SubElement(full_words[word_index], 'mor')
                mword.text = w

            u.remove(morphology)


    def _morphology_inference(self, u):
        # go through words on gloss tier
        words = u.findall('.//w')
        word_index = -1
        for wd in words:

            word_index += 1

            if ('warning' in wd.attrib.keys() 
                    and wd.attrib['warning'] == 'not glossed'):
                word_index += 1
                continue

            w = wd.find('mor')

            if w is None:
                word_index += 1
                continue

        # colon:
        #   in POS tag -> . (= subcategory)
            #   after stem -> . (= non-concatenative morphology)
            #   in suffix -> . (= subgloss)
            # ==> keep for now, this should be done by postprocessing
            
            # split into POS tag and gloss
            if '|' in w.text:
                parts = w.text.partition('|')
                stem_pos = parts[0]
                gloss = parts[2]
            elif '/' in w.text:
                parts = w.text.partition('/')
                stem_pos = parts[0]
                gloss = parts[2]
            else:
                stem_pos = None
                gloss = w.text
        
            # morphemes per word
            # split into stem and possible suffixes; split suffix chain if exists
            check_stem = re.search('^([^\\-]+)(.*)$', gloss)
            (stem, suffix_string) = ('', '')
            if check_stem:
                stem = check_stem.group(1)
                suffix_string = check_stem.group(2)
        
                # add stem, gloss (unknown), and POS for stem to corpus dic
                m = etree.SubElement(w, 'm')
                m.attrib['segments_target'] = stem
                m.attrib['glosses_target'] = '???'
                m.attrib['pos_target'] = stem_pos
        
            if suffix_string:
                # drop first hyphen in suffix string so split() doesn't produce empty elements
                suffix_string = suffix_string.lstrip("-")
                for suffix_gloss in suffix_string.split('-'):
                    m = etree.SubElement(w, 'm')
                    m.attrib['segments_target'] = '???'
                    m.attrib['glosses_target'] = suffix_gloss
                    m.attrib['pos_target'] = 'sfx'

            w.text = ''

        # EOF word loop
        
        # go through words <w> and insert glosses for repetitions and retracings (warning 'not glossed; repeat/search ahead')

        # EOF glosses for repetitions/retracings 

        # check alignment with words that were found in <w>
        # if there is no morphology, add warning to complete utterance


    # EOF Turkish_KULLD
    

if __name__ == '__main__':

    from parsers import CorpusConfigParser as Ccp
    conf = Ccp()
    conf.read('ini/Turkish.ini')
    corpus = TurkishCleaner(conf, 'tests/corpora/Turkish_KULLD/xml/Turkish_KULLD.xml')

    corpus._debug_xml()

