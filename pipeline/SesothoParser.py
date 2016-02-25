# -*- coding: utf-8 -*-

import re
import sys
import itertools
import pdb

from lxml import etree
from XMLParser import XMLParser

class SesothoParser(XMLParser):

    def _get_annotations(self, u):
        morph = {}
        trans = None
        comment = None
        for a in u.findall('.//a'):
            for tier in self.cfg['morphology_tiers']:
                if a.attrib.get('type') == tier:
                    morph[tier] = a.text
            if (a.attrib.get('type') == 'english translation'):
                trans = a.text
            if (a.attrib.get('type') == 'situation'):
                comment = a.text
        return morph, trans, comment

    def _morphology_inference(self, u):

        # Sesotho has two morphology tiers, "target gloss" (= segments) and "coding" (= glosses and POS). Parse and align.             
        # Segments. The Sesotho segment tier doesn't make a clear distinction between affixes and stems, so its elements can't be added to the corpus dic until they have been compared with the glosses. Store them in a temporary Vividict().
        segment_tier = u['morphology']['morphemes']
        segwords = []
        if segment_tier is not None:                
            # split into words
            word_index = 0
            segment_words = re.split('\\s+', segment_tier)
            
            for w in segment_words:
                # Check brackets. In Sesotho, these are only used to mark contractions of the verb 'go' which are conventional in both child and adult speech. The form of 'go' is given in brackets from the first to the last morpheme, is completely covert, and does not correspond to an element in <w>, so drop it altogether. The following, partially bracketed INF (if-) has an effect on the contracted surface form, so only remove the brackets but keep the gloss.
                if re.search('^\(.*\)$', w):
                    continue

                segwords.append([])
                w = re.sub('[\(\)]', '', w)
                
                # split into morphemes
                morpheme_index = 0
                for m in re.split('\\-', w):
                    segwords[word_index].append(m)
                    morpheme_index += 1
                word_index += 1
                    
        # Glosses and POS
        gloss_tier = u['morphology']['gloss_raw']
        if gloss_tier is not None:
            
            # first remove spaces in noun class brackets
            gloss_tier = re.sub('\\s+,\\s+', ',', gloss_tier)
            # replace / as noun class separator by | so it can't be confused with / as a morpheme separator
            gloss_tier = re.sub('(\d+a?)\\/(\d+a?)', '\\1|\\2', gloss_tier)
            
            # the remaining spaces indicate word boundaries -> split
            gloss_words = re.split('\\s+', gloss_tier)
            
            # check alignment between segments and glosses on word level
            if len(gloss_words) != len(segment_words):
                print('alignment problem in ' + file_name + ', utterance ' + str(utterance_id) + ': tier "target gloss" (= segments_target) has ' +
                    str(len(segment_words)) + ' words vs. ' + str(len(gloss_words)) + ' in "coding" (= glosses_target)')
                XMLParser.creadd(u['utterance'], 'warning', 'broken alignment segments_target : glosses_target')
            
            # reset word index for writing to corpus dict
            word_index = -1
                
            # go through words
            # mwords is a list of lists of morphemes
            mwords = []
            for w in gloss_words:
                                    
                # ignore punctuation in the segment/gloss tiers; this shouldn't be counted as morphological words
                if re.search('^[.!\?]$', w):
                    continue
                
                # Check brackets. In Sesotho, these can be used to mark contractions of the verb 'go' (see above under segments). 
                # Skip fully bracketed form of 'go'
                if re.search('^\(.*\)$', w):
                    continue
                # Keep partially bracketed INF, removing brackets. A more precise regex is required for removing brackets from the gloss tier because there they can also indicate noun classes.
                w = re.sub('\(([a-zA-Z]\\S+)\)', '\\1', w)
                                    
                # split into morphemes
                passed_stem = False
                glosses = re.split('[\\-]', w)

                # count up word index, extend list if necessary
                word_index += 1
                
                # check alignment between segments and glosses on morpheme level
                if len(glosses) != len(segwords[word_index]):
                   # print('alignment problem in ' + file_name + ', utterance ' + str(utterance_id) + ', word ' + str(word_index) +
                   #     ': tier "target gloss" (= segments_target) has ' + str(len(segments[word_index])) + ' morphemes vs. ' + str(len(glosses)) + 
                   #     ' in "coding" (= glosses_target)')
                    XMLParser.creadd(u['words'][word_index], 'warning', 'broken alignment segments_target : glosses_target')
                
                # morphemes is a list of morphemes; initial index is -1
                morphemes = []
                morpheme_index = -1
                    
                for gloss in glosses:
                    # check whether present element is the stem; if no, set POS to prefix/suffix
                    pos = ''
                    if (len(glosses) == 1 or re.search('(v|id)\^|\(\d', gloss)
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
                    if re.search('a_(Game|Name|Place|Song)', gloss): gloss = gloss.lower()                            
                    
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
                    
                    # count up morpheme index, extend list if necessary
                    morpheme_index += 1
                    morpheme = {}
                    # now put together segment, gloss, and POS
                    morpheme['glosses_target'] = gloss
                    morpheme['pos_target'] = pos                        
                    # if there happen to be more glosses than segments (-> misalignment), the segment indices don't go as far as the gloss indices, so first check
                    if segwords[word_index][morpheme_index]: 
                        morpheme['segments_target'] = segwords[word_index][morpheme_index]
                    else: 
                        morpheme['segments_target'] = ''

                    morphemes.append(morpheme)
            
                mwords.append(morphemes)
            # EOF word loop
            
            # check alignment between glosses and words that were found in <w>. This can be done only now because glosses contain punctuation (dropped in the end) but <w> doesn't. 
            # alignment between <w> and segments doesn't have to be checked separately because glosses:segments is already checked above and good alignment for both glosses:segments and glosses:<w> entails good alignment for segments:<w>
            if (word_index+1) != len(u['words']):
                #print('alignment problem in ' + file_name + ', utterance ' + str(utterance_id) + ': general word tier <w> has ' 
                #    + str(len(u['words'])) + ' words vs ' + str(word_index+1) + ' in "coding" (= glosses_target)')
                XMLParser.creadd(u['utterance'], 'warning', 'broken alignment full_word : glosses_target')

            return mwords

        # if there is no morphology, add warning to complete utterance
        elif gloss_tier is None:
            XMLParser.creadd(u['utterance'], 'warning', 'not glossed')
            return []
    # EOF Sesotho        
