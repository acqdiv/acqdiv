# -*- coding: utf-8 -*-

import copy
import re
import sys
import itertools

from lxml import etree
from xml_parser import XMLParser

class TurkishParser(XMLParser):

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
                    w.attrib['target'] = '???'
                    w.attrib['glossed'] = 'no'
                    continue
            if 'formType' in w.attrib and (w.attrib['formType'] 
                    in ['interjection', 'onomatopoeia', 'family-specific']):
                w.attrib['target'] = '???'
                w.attrib['glossed'] = 'no'
                continue
        return words

    def _morphology_inference(self, u):
        morphemes = []
        morphstring = u['morphology']['morphemes']

        if morphstring == None or morphstring == '':
            u['utterance']['warning'] = 'not glossed'
            return []

        morphstring = re.sub('(^|\\s)[\.\?!:\+\/]+(\\s|$)', '\\1\\2', morphstring) # utterance delimiters and codes
        morphstring = re.sub('(^|\\s)tag\|\\S+(\\s|$)', '\\1\\2', morphstring) # tags
        morphstring = re.sub('\\s+$', '', morphstring)
        # other clutter
        morphstring = re.sub('&', '.', morphstring) # joins glosses
        morphstring = re.sub('\+', '_', morphstring) # marks word number mismatches between orthography and morphology (but is less frequent than "_")
        morphstring = re.sub('([A-Z]\\S*):\\s+', '\\1', morphstring) # POS tags gone astray: join with following word
        morphstring = re.sub('([^\|]+)\|([^\|]+)\|', '\\1/\\2|', morphstring) # double POS tags: replace "|" by "/"
                        
        # split mor tier into words, reset counter to -1
        mwords = re.split('\\s+',morphstring)
        
        # go through words on gloss tier
        ic = itertools.count()
        length_morphology = len(mwords)
        while True:
            i = next(ic)
            if i >= length_morphology or i >= len(u['words']):
                break
            w = mwords[i]
            try:
                if u['words'][i]['warning'] == 'not glossed':
                    mwords.insert(i, '')
                    length_morphology += 1
                    continue
            except KeyError:
                pass

            if '_' in w:
                wmors = w.split('_')
                if '_'  in u['words'][i]['full_word_target']:
                    pass
                else:
                    for j in range(len(wmors)):
                        mwords.insert(i+j, wmors[j])
                        
            # colon:
            #   in POS tag -> . (= subcategory)
            #   after stem -> . (= non-concatenative morphology)
            #   in suffix -> . (= subgloss)
            # ==> keep for now, this should be done by postprocessing
            
            # split into POS tag and gloss
            if '|' in w:
                parts = w.partition('|')
                stem_pos = parts[0]
                gloss = parts[2]
            elif '/' in w:
                parts = w.partition('/')
                stem_pos = parts[0]
                gloss = parts[2]
            else:
                stem_pos = None
                gloss = w
        
            # morphemes per word
            word_mors = []
            # split into stem and possible suffixes; split suffix chain if exists
            check_stem = re.search('^([^\\-]+)(.*)$', gloss)
            (stem, suffix_string) = ('', '')
            if check_stem:
                stem = check_stem.group(1)
                suffix_string = check_stem.group(2)
        
                # add stem, gloss (unknown), and POS for stem to corpus dic
                mdic = {}
                mdic['segments_target'] = stem
                mdic['glosses_target'] = '???'
                mdic['pos_target'] = stem_pos
                word_mors.append(mdic)
        
            if suffix_string:
                # drop first hyphen in suffix string so split() doesn't produce empty elements
                suffix_string = suffix_string.lstrip("-")
                for suffix_gloss in suffix_string.split('-'):
                    mdic = {}
                    mdic['segments_target'] = '???'
                    mdic['glosses_target'] = suffix_gloss
                    mdic['pos_target'] = 'sfx'
                    word_mors.append(mdic)

            if word_mors != []:
                morphemes.append(word_mors)

        # EOF word loop
        
        # go through words <w> and insert glosses for repetitions and retracings (warning 'not glossed; repeat/search ahead')
        for i in range(0, len(u['words'])):
            
            if('warning' in u['words'][i].keys() and
                re.search('not glossed; (repeat|search ahead)', u['words'][i]['warning'])):
                
                # count up number of glossed words
                length_morphology += 1
                
                # (1) repetitions: get morphology from preceding word 
                if 'repeat' in  u['words'][i]['warning']:
                    if i != 0:
                        morphemes.insert(i, morphemes[i-1].copy())
                
                # (2) retracings: get morphology from any matching word further ahead
                if 'search ahead' in u['words'][i]['warning']:
                    # go through all following <w> 
                    for j in range(i, len(u['words'])):
                        # corresponding target words: transfer morphology
                        if u['words'][j]['full_word_target'] == u['words'][i]['full_word_target']:
                            # transfer gloss from match to present word
                            try:
                                morphemes.insert(i, morphemes[j].copy())
                            except IndexError:
                                print("Skipping unglossed retracing in file "
                                        "{} utterance {} words {}, {}: "
                                        "next word is unglossed".format(
                                            self.sname, 
                                            u['utterance']['source_id'], i, j))
                                print(len(morphemes), len(u['words']))
                        # corresponding actual words: transfer morphology AND target word
                        elif u['words'][j]['full_word'] == u['words'][i]['full_word']:
                            # transfer gloss and target from match to present word
                            morphemes.insert(i, morphemes[j].copy())
                            u['words'][i]['full_word_target'] = u['words'][j]['full_word_target']
                    
                #remove warning and delete key if empty
                u['words'][i]['warning'] = re.sub(';?\\s*not glossed; (repeat|search ahead)', '', u['words'][i]['warning'])

            if u['words'][i]['warning'] == '':
                del u['words'][i]['warning']

        # EOF glosses for repetitions/retracings 

        # check alignment with words that were found in <w>
        if len(morphemes) != len(u['words']):
            u['utterance']['warning'] = 'broken alignment full_word : segments/glosses'

        # if there is no morphology, add warning to complete utterance
        if len(morphemes) == 0:
            u['utterance']['warning'] = 'not glossed'

        return morphemes
            
    # EOF Turkish_KULLD
