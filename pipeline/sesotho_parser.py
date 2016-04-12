# -*- coding: utf-8 -*-

import re
import sys
import itertools
import pdb

from lxml import etree
from xml_parser import XMLParser

class SesothoParser(XMLParser):

    def _process_morphology(self, u):
    
        full_words = u.findall('.//w')
        wlen = len(full_words)

        segment_tier = u.find("a[@type='target gloss']")
        if segment_tier is not None:                
            # split into words
            word_index = -1
            segment_words = re.split('\\s+', segment_tier.text)
            
            for w in segment_words:
                # Check brackets. In Sesotho, these are only used to mark contractions of the verb 'go' which are conventional in both child and adult speech. The form of 'go' is given in brackets from the first to the last morpheme, is completely covert, and does not correspond to an element in <w>, so drop it altogether. The following, partially bracketed INF (if-) has an effect on the contracted surface form, so only remove the brackets but keep the gloss.
                if re.search('^(\(.*\)|[\.\?])$', w):
                    continue
                else:
                    w = re.sub('[\(\)]', '', w)

                word_index, wlen = XMLParser.word_index_up(
                        full_words, wlen, word_index, u)

                mor = etree.SubElement(full_words[word_index], 'mor')
                seg = etree.SubElement(mor, 'seg')
                seg.text = w
                
            u.remove(segment_tier)
                    
        # Glosses and POS
        gloss_tier = u.find("a[@type='coding']")    
        if gloss_tier is not None:
            # set word index for inspecting temporary dict
            word_index = 0
            
            # first remove spaces in noun class brackets
            gloss_tier.text = re.sub('\\s+,\\s+', ',', gloss_tier.text)
            # replace / as noun class separator by | so it can't be confused with / as a morpheme separator
            gloss_tier.text = re.sub('(\d+a?)\\/(\d+a?)', '\\1|\\2', gloss_tier.text)
            
            # the remaining spaces indicate word boundaries -> split
            gloss_words = re.split('\\s+', gloss_tier.text)
            
            # check alignment between segments and glosses on word level
            if len(gloss_words) != len(segment_words):
                print('alignment problem in ' + file_name + ', utterance ' + str(utterance_id) + ': tier "target gloss" (= segments_target) has ' +
                    str(len(segment_words)) + ' words vs. ' + str(len(gloss_words)) + ' in "coding" (= glosses_target)')
                creadd(corpus[text_id][utterance_index], 'warnings', 'broken alignment segments_target : glosses_target')
            
            # reset word index for writing to corpus dict
            word_index = -1
                
            # go through words
            for w in gloss_words:
                                    
                # ignore punctuation in the segment/gloss tiers; this shouldn't be counted as morphological words
                if re.search('^[.!\?]$', w):
                    continue
                
                # Check brackets. In Sesotho, these can be used to mark contractions of the verb 'go' (see above under segments). 
                # Skip fully bracketed form of 'go'
                if re.search('^\(.*\)$', w):
                    continue
                # Keep partially bracketed INF, removing brackets. A more precise regex is required for removing brackets from the gloss tier because there they can also indicate noun classes.
                else:
                    w = re.sub('\(([a-zA-Z]\\S+)\)', '\\1', w)
                                    
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
                seg = mor.find('seg')
                gl  = mor.find('gl')

            # split into morphemes
            segments = re.split('\\-', seg.text)
            glosses = re.split('[\\-]', gl.text)
            passed_stem = False

            
            # check alignment between segments and glosses on morpheme level
            if len(glosses) != len(segments):
                XMLParser.creadd(fw.attrib, 'warnings', 
                        'broken alignment segments_target : glosses_target')
            
            ms = itertools.zip_longest(glosses, segments, fillvalue='')
            for gloss, segment in ms:
                # check whether present element is the stem; if no, set POS to prefix/suffix
                pos = ''
                if len(glosses)==1 or (re.search('(v|id)\^|\(\d', gloss) 
                        or re.match('(aj$|nm$|ps\d+)', gloss)):
                    passed_stem = True
                elif passed_stem == False:
                    pos = 'pfx'
                elif passed_stem == True:
                    pos = 'sfx'

                # n^ prefixed to all noun class glosses is completely redundant, so delete
                gloss = re.sub('[nN]\^(?=\\d)', '', gloss)
                # n^ prefixed to all proper names: replace by 'a_', lowercase label
                gloss = re.sub('[nN]\^([gG]ame|[nN]ame|[pP]lace|[sS]ong)', 'a_\\1', gloss)
                if re.search('a_(Game|Name|Place|Song)', gloss): 
                    gloss = gloss.lower()                            
                
                # get remaining POS and remove indicators and other clutter in the morpheme string
                pos_dic = {'aj' : 'adj' , 'av' : 'adv'  ,  'cd' : 'ptcl',
                           'cj' : 'conj', 'cm' : 'ptcl' ,  'd'  : 'dem' ,
                           'ht' : 'ptcl', 'ij' : 'intj' ,  'loc': 'ptcl', 
                           'lr' : 'rel' , 'ng' : 'ptcl' ,  'nm' : 'num' ,
                           'obr': 'rel' , 'or' : 'rel'  ,  'pn' : 'pro' ,
                           'pr' : 'prep', 'ps' : 'poss' ,  'q'  : 'ptcl',
                           'sr' : 'rel' , 'wh' : 'intrg'                 }
                # affixes already have their POS, but replace '_' as concatenator by more standard '.'
                if pos=='pfx' or pos=='sfx':
                    gloss = re.sub('_', '.', gloss)
                # verbs have v^, one typo as s^
                elif re.search('[vs]\^', gloss): 
                    pos = 'v'
                    gloss = re.sub('[vs]\^', '', gloss)
                # nouns contains "(\d)" (default) or "ps/" (suppletive possession); remove these after setting POS
                elif re.search('\(\d+', gloss) or re.search('^ps\/', gloss):
                    pos = 'n'
                # words with nominal concord
                elif re.search('^(d|lr|obr|or|pn|ps|sr)\d+', gloss):
                    pos_match = re.search('^(d|lr|obr|or|pn|ps|sr)\d+', gloss)
                    pos = pos_match.group(1)
                    gloss = re.sub(pos, '', gloss)
                # various particles, mostly without a precise gloss
                elif re.search('^(aj|av|cd|cj|cm|ht|ij|loc|lr|ng|nm|obr|or|pr|q|sr|wh)$', gloss):
                    pos = gloss
                # free person markers (rare)
                elif re.search('^sm\d+[sp]?$', gloss):
                    pos = 'afx.detached'
                # copula
                elif re.search('^cp|cp$', gloss):
                    pos = 'cop'
                # ideophones
                elif re.search('id\^', gloss): 
                    pos = 'ideoph'
                # punctuation marks
                elif re.search('^[.!\?]$', gloss):
                    pos = 'punct'
                # meaningless and unclear words. Note that "xxx" in the Sesotho coding tier is not the same as CHAT "xxx" in the transcription tier - it does not stand for words that could not be transcribed but for words with unclear meaning. 
                elif gloss == 'word' or gloss == 'xxx':
                    pos = 'none'
                    gloss = '???'
                else:
                    pos = '???'
                
                m = etree.SubElement(mor, 'm')
                # now put together segment, gloss, and POS
                m.attrib['glosses_target'] = gloss
                m.attrib['pos_target'] = pos                        
                m.attrib['segments_target'] = segment
                            
                    # EOF word loop
            mor.remove(seg)
            mor.remove(gl)
            # EOF Sesotho        

if __name__ == "__main__":

    from parsers import CorpusConfigParser as Ccp
    conf = Ccp()
    conf.read('ini/Sesotho.ini')
    corpus = SesothoParser(conf, 'tests/corpora/Sesotho/xml/Sesotho.xml')

    corpus._debug_xml()

