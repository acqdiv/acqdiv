# -*- coding: utf-8 -*-
import copy
import re
import sys
import itertools
import pdb

from lxml import etree
from xml_cleaner import XMLCleaner

class InuktitutCleaner(XMLCleaner):

    def _mark_retracings(self, u):
        pass

    def _process_morphology(self, u):
        
        # take over tier "coding" (= general syntactic coding). This tier cannot be treated in the shared XML part because it has very different contents across corpora.  
        #tier = u.find("a[@type='coding']")
        #if tier is not None: 
        #    u['utterance']['syntax_coding'] = tier.text
        
        # parse the morphology tier mor
        full_words = u.findall('.//w')
        morphology = u.find("a[@type='extension'][@flavor='mor']")
        if morphology is not None and not morphology.text.startswith('xxx'):
            
            # remove CHAT garbage
            morphology.text = re.sub('\[\+.*?\"\]', '', morphology.text) # postcodes in square brackets; these are not documented anywhere
            morphology.text = re.sub('\[\/+\]', '', morphology.text) # repetition marker
            morphology.text = re.sub('\[\*\]', '', morphology.text) # error coding
            morphology.text = re.sub('\+[\.,\?!;:\///\"]+', '', morphology.text) # other codes starting with "+"
            morphology.text = re.sub('\[\+.+?\]', '', morphology.text) # plus codes in square brackets
            morphology.text = re.sub('\[\\s*=![^\]]*\]', '', morphology.text) # comment on action
            morphology.text = re.sub('(^|\\s)[#\/](\\s|$)', ' ', morphology.text) # pause markers
            morphology.text = re.sub('@e', '', morphology.text) # "English" tag is semantically not part of glosses -> delete
            morphology.text = re.sub('(\\s|^)&(amp;)?(?P<form>\\S+)', ' ???|\g<form>^???', morphology.text) # occasional fragment glosses - convert to "POS and gloss unknown + form"
            morphology.text = re.sub('\[=\?\\s+(\\S*?)\\s*\]', '[=?\\1]', morphology.text) # possible target to be processed further below; only remove initial space
            morphology.text = re.sub('(\[=\?.*?\]\\s*)(\[=\?.*?\])+', '\\1', morphology.text) # in case of several possible targets, only keep the first
            morphology.text = re.sub('[<>]|&[lg]t;', '', morphology.text) # useless XML entities; keep &amp; 
            morphology.text = re.sub('(?<=[\\s\\]a-zA-Z\?])[\.!]+(?=\\s|$)', '', morphology.text) # utterance delimiters .!
            morphology.text = re.sub('(?<=[\\s\\]a-zA-Z])\?(?=\\s|$)', '', morphology.text) # utterance delimiter ?                
            morphology.text = re.sub('^\\s*[\?\.!]+\\s*$', '', morphology.text) # utterances consisting of delimiter(s) only
            morphology.text = re.sub('xxx|\S+\?{2,}|\?{4,}', '???', morphology.text) # words with unclear gloss
            morphology.text = re.sub('0\.', '', morphology.text) # empty utterance; this is already indicated on main tier
            morphology.text = re.sub('\\b0\\b', '', morphology.text) # empty utterance
            # insecure glosses [?]: add warning, then remove
            if re.search('\[\?\]', morphology.text):
                 XMLCleaner.creadd(u.attrib, 'warning', 'gloss insecure')
                 morphology.text = re.sub('\[\?\]', '', morphology.text)
            
            # strip white space from both ends
            morphology.text = morphology.text.lstrip()
            morphology.text = morphology.text.rstrip()
            
            # check if anything's left; if not, place warning and break loop
            if morphology.text == '':
                XMLCleaner.creadd(u.attrib, 'warning', 'not glossed')
                return
            
            # split mor tier into words, reset counters to 0
            words = re.split('\\s+', morphology.text)
            word_index = -1
            wlen = len(full_words)
            
            # go through words on gloss tier
            for w in words:
                
                # words of the form [=? ...] are target glosses for the last word -> set a flag and decrease word index
                target_gloss = False
                if re.search('^\[=\?.*\]$', w):
                    target_gloss = True
                    word_index -= 1
                    w = re.sub('^\[=\?(.*)\]$', '\\1', w)

                # count up word index, extend list if necessary
                word_index, wlen = XMLCleaner.word_index_up(
                        full_words, wlen, word_index, u)
                # some words in <w> warning "not glossed": this means there is no element on the morphology tier corresponding to the present <w>
                # -> incremeent the <w> counter by one as long as the present morphological word is associated with the next <w>
                try:
                    while('warning' in full_words[word_index].attrib and
                        re.search('not glossed',full_words[word_index].attrib['warning'])):
                        word_index += 1
                except IndexError:
                    return

                if not target_gloss:
                    mword = etree.SubElement(full_words[word_index], 'mor')
                    mword.text = w
                else:
                    mor = full_words[word_index].find('mor')
                    mword = etree.SubElement(mor, 'tgloss')
                    mword.text = w

            u.remove(morphology)
        
        else:
            XMLCleaner.creadd(u.attrib, 'warning', 'not glossed')
                                                        
    # EOF Inuktitut 

    def _morphology_inference(self, u):

        full_words = u.findall('.//w')
        for fw in full_words:

            mor = fw.find('mor')
            tg = fw.find('tgloss')

            # split into morphemes by "+"
            if mor is not None:
                w = mor.text
                morphemes = re.split('\+', w)

                # go through morphemes
                for mph in morphemes: 
                    
                    # split each block into POS|form^gloss
                    pos, form, gloss = '???', '???', '???'
                    m_struc = re.search('^(.*)\|(.*)\^(.*)$', mph)
                    if m_struc is not None:
                        if m_struc.group(1) is not None:
                            pos = m_struc.group(1)
                            # if there are subPOS marked by "|", use "." as separator instead
                            pos = re.sub('\|', '.', pos)
                        if m_struc.group(2) is not None:
                            form = m_struc.group(2)
                        if m_struc.group(3) is not None:
                            gloss = m_struc.group(3)
                            # replace "&" and "&amp;" (= "&", separator between stem and grammatical gloss) by LGR "."
                            gloss = re.sub('&(amp;)?', '.', gloss)
                            # remove @e (marker for English words)
                            gloss = re.sub('@', '', gloss)
                    else:
                        if not re.search('^\?\?\?$', mph):
                            XMLCleaner.creadd(fw.attrib, 'warning', 'contains unstructured morpheme')
                    mor.text = ''
                
                # default: add morpheme to corpus dic
                    m = etree.SubElement(mor, 'm')
                    m.attrib['pos_target'] = pos
                    m.attrib['segments_target'] = form
                    m.attrib['glosses_target'] = gloss                             
                # if the present word is a target gloss, correct the last gloss set from "target" to "actual" and set its target to the present gloss set
            if tg is not None:
                w = tg.text
                morphemes = re.split('\+', w)
                mors = fw.findall('m')
                morpheme_index = -1
                for mph in morphemes:
                    morpheme_index += 1
                    pos, form, gloss = '???', '???', '???'
                    m_struc = re.search('^(.*)\|(.*)\^(.*)$', mph)
                    if m_struc is not None:
                        if m_struc.group(1) is not None:
                            pos = m_struc.group(1)
                            # if there are subPOS marked by "|", use "." as separator instead
                            pos = re.sub('\|', '.', pos)
                        if m_struc.group(2) is not None:
                            form = m_struc.group(2)
                        if m_struc.group(3) is not None:
                            gloss = m_struc.group(3)
                            # replace "&" and "&amp;" (= "&", separator between stem and grammatical gloss) by LGR "."
                            gloss = re.sub('&(amp;)?', '.', gloss)
                            # remove @e (marker for English words)
                            gloss = re.sub('@', '', gloss)
                    else:
                        if not re.search('^\?\?\?$', mph):
                            XMLCleaner.creadd(fw.attrib, 'warning', 'contains unstructured morpheme')
                    m = mors[morpheme_index]
                    m.attrib['pos'] = m.attrib['pos_target']
                    m.attrib['pos_target'] = pos
                    m.attrib['segments'] = m.attrib['segments_target']
                    m.attrib['segments_target'] = form
                    m.attrib['glosses'] = m.attrib['glosses_target']
                    m.attrib['glosses_target'] = gloss                           

                fw.remove(tg)
                
        # EOF word loop
    
if __name__ == '__main__':

    from parsers import CorpusConfigParser as Ccp
    conf = Ccp()
    conf.read('ini/Inuktitut.ini')
    corpus = InuktitutCleaner(conf, 'tests/corpora/Inuktitut/xml/Inuktitut.xml')

    corpus._debug_xml()

