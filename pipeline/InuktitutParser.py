# -*- coding: utf-8 -*-

import copy
import re
import sys
import itertools
import pdb

from lxml import etree
from XMLParser import XMLParser

class InuktitutParser(XMLParser):

    def _clean_retracings(self, group):
        pass

    def _morphology_inference(self, u):
        
        # take over tier "coding" (= general syntactic coding). This tier cannot be treated in the shared XML part because it has very different contents across corpora.  
        #tier = u.find("a[@type='coding']")
        #if tier is not None: 
        #    u['utterance']['syntax_coding'] = tier.text
        
        # parse the morphology tier mor
        morphology = u['morphology']['morphemes']
        if (morphology is not None) and (not morphology.startswith('^xxx.')):
            
            # remove CHAT garbage
            morphology = re.sub('\[\+.*?\"\]', '', morphology) # postcodes in square brackets; these are not documented anywhere
            morphology = re.sub('\[\/+\]', '', morphology) # repetition marker
            morphology = re.sub('\[\*\]', '', morphology) # error coding
            morphology = re.sub('\+[\.,\?!;:\///\"]+', '', morphology) # other codes starting with "+"
            morphology = re.sub('\[\+.+?\]', '', morphology) # plus codes in square brackets
            morphology = re.sub('\[\\s*=![^\]]*\]', '', morphology) # comment on action
            morphology = re.sub('(^|\\s)[#\/](\\s|$)', ' ', morphology) # pause markers
            morphology = re.sub('@e', '', morphology) # "English" tag is semantically not part of glosses -> delete
            morphology = re.sub('(\\s|^)&(amp;)?(?P<form>\\S+)', ' ???|\g<form>^???', morphology) # occasional fragment glosses - convert to "POS and gloss unknown + form"
            morphology = re.sub('\[=\?\\s+(\\S*?)\\s*\]', '[=?\\1]', morphology) # possible target to be processed further below; only remove initial space
            morphology = re.sub('(\[=\?.*?\]\\s*)(\[=\?.*?\])+', '\\1', morphology) # in case of several possible targets, only keep the first
            morphology = re.sub('[<>]|&[lg]t;', '', morphology) # useless XML entities; keep &amp; 
            morphology = re.sub('(?<=[\\s\\]a-zA-Z\?])[\.!]+(?=\\s|$)', '', morphology) # utterance delimiters .!
            morphology = re.sub('(?<=[\\s\\]a-zA-Z])\?(?=\\s|$)', '', morphology) # utterance delimiter ?                
            morphology = re.sub('^\\s*[\?\.!]+\\s*$', '', morphology) # utterances consisting of delimiter(s) only
            morphology = re.sub('xxx|\S+\?{2,}|\?{4,}', '???', morphology) # words with unclear gloss
            morphology = re.sub('0\.', '', morphology) # empty utterance; this is already indicated on main tier
            morphology = re.sub('\\b0\\b', '', morphology) # empty utterance
            # insecure glosses [?]: add warning, then remove
            if re.search('\[\?\]', morphology):
                 XMLParser.creadd(u['utterance'], 'warning', 'gloss insecure')
                 morphology = re.sub('\[\?\]', '', morphology)
            
            # strip white space from both ends
            morphology = morphology.lstrip()
            morphology = morphology.rstrip()
            
            # check if anything's left; if not, place warning and break loop
            if morphology == '':
                XMLParser.creadd(u['utterance'], 'warning', 'not glossed')
                return []
            
            # split mor tier into words, reset counters to 0
            words = re.split('\\s+', morphology)
            word_index = -1
            #length_morphology = 0
            mwords = []
            
            # go through words on gloss tier
            for w in words:

                word_index += 1
                
                # words of the form [=? ...] are target glosses for the last word -> set a flag and decrease word index
                target_gloss = False
                if re.search('^\[=\?.*\]$', w):
                    target_gloss = True
                    word_index -= 1
                    w = re.sub('^\[=\?(.*)\]$', '\\1', w)
                                    
                # some words in <w> warning "not glossed": this means there is no element on the morphology tier corresponding to the present <w>
                # -> increment the <w> counter by one as long as the present morphological word is associated with the next <w>
                try:
                    while('warning' in u['words'][word_index].keys() and
                        u['words'][word_index]['warning'] == 'not glossed'):
                         word_index += 1
                         mwords.append([])
                except IndexError:
                    pass
                                                        
                # split into morphemes by "+"
                morphemes = re.split('\+', w)
                
                # mdics is a list of morphemes; initial index is -1
                mdics = []
                morpheme_index = -1
                
                # go through morphemes
                for m in morphemes:

                    morpheme_index += 1

                    mdic = {}
                    
                    # split each block into POS|form^gloss
                    pos, form, gloss = '???', '???', '???'
                    m_struc = re.search('^(.*)\|(.*)\^(.*)$', m)
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
                            gloss = re.sub('@e', '', gloss)
                    else:
                        if not re.search('^\?\?\?$', m):
                            #print(file_name, utterance_index, ": gloss", m, "appears to be unstructured; morphemes:", morphemes)
                            try:
                                XMLParser.creadd(u['words'][word_index], 'warning', 'contains unstructured morpheme')
                            except IndexError:
                                pass
                    
                    # default: add morpheme to corpus dic
                    if not target_gloss:
                        mdic['pos_target'] = pos
                        mdic['segments_target'] = form
                        mdic['glosses_target'] = gloss                             
                        mdics.append(mdic)
                    # if the present word is a target gloss, correct the last gloss set from "target" to "actual" and set its target to the present gloss set
                    elif target_gloss:
                        # the target_gloss code sets word_index to one less
                        # so this modifies items in the preceding word
                        #pdb.set_trace()
                        try:
                            mdic = mwords[word_index][morpheme_index]
                            empty_actual = False
                        except IndexError:
                            mwords[word_index].append({})
                            mdic = mwords[word_index][morpheme_index]
                            empty_actual = True
                        if not empty_actual:
                            mdic['pos'] = mdic['pos_target']
                            mdic['segments'] = mdic['segments_target']
                            mdic['glosses'] = mdic['glosses_target']
                        mdic['pos_target'] = pos
                        mdic['segments_target'] = form
                        mdic['glosses_target'] = gloss

                if not target_gloss:
                    mwords.append(mdics)
                
            # EOF word loop
            
            # check alignment with words that were found in <w>
            # note: alignment on morpheme-level doesn't have to be checked at all for Inuktitut because the segment and gloss tiers are not separate
            if len(mwords) != len(u['words']):
                #print('alignment problem in ' + file_name + ', utterance ' + str(utterance_id) + ': general word tier <w> has '
                #    + str(u['utterance']['length_in_words']) + ' words vs ' + str(length_morphology) + ' in "mor" (= morphology)')
                XMLParser.creadd(u['utterance'], 'warning', 'broken alignment full_word : segments/glosses')

            return mwords

            # if there is no morphology, add warning to complete utterance
        else:
                XMLParser.creadd(u['utterance'], 'warning', 'not glossed')
                return []
            
        # EOF Inuktitut 
