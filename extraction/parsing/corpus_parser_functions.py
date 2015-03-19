#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
A collection of functions for parsing CHAT, Toolbox, and XML corpora. This script does not work independently but is called by other scripts via:

from corpus_parser_functions import parse_corpus

Author: Robert Schikowski <robert.schikowski@uzh.ch>
'''


################
### Packages ###
################

import codecs
import collections
import os
import re
import xml.etree.ElementTree as ET


###############
### Classes ###
###############

# class for dictionaries with autovivification
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


########################
### Global variables ###
########################

# correspondences between XML standard dependent tiers (shared across corpora) and JSON
xml_dep_correspondences = {
    'actions' : 'comments',
    'addressee' : 'addressee',
    'comments' : 'comments',
    'english translation' : 'english',
    'explanation' : 'comments',
    'gesture' : 'gestures',
    'orthography' : 'orthographic',
    'situation' : 'comments',
    'time stamp' : 'starts_at'
}
            # correspondences between XML extended dependent tiers and JSON
xml_ext_correspondences = {
    'pho' : 'phonetic'  
}
# correspondences between other XML elements and JSON
xml_other_correspondences = {
    'actmor' : 'segments',
    'actual' : 'phonetic',
    'model' : 'phonetic_target',
    'mormea' : 'glosses_target',
    'mortyp' : 'pos_target',
    'tarmor' : 'segments_target'
}

# correspondences between values of XML <t> (= sentence type) and JSON
t_correspondences = {
    'p' : 'default', # CHAT .
    '.' : 'default',
    'q' : 'question', # CHAT ?
    '?' : 'question', 
    'e' : 'exclamation', # CHAT !
    '!' : 'exclamation',
 	'trail off' : 'trail off', # CHAT +...
 	'interruption' : 'interruption', # CHAT +/.
 	'self interruption' : 'self interruption', # CHAT +//.
 	'quotation precedes' : 'quotation precedes', # CHAT +".
 	'quotation next line' : 'quotation next line', # CHAT +"/.
 	'interruption question' : 'interruption question' # CHAT +/?
}

# correspondences between Toolbox utterance-level tiers and JSON
# a simple dictionary isn't enough here because the meaning of tiers changes according to the corpus
tbx_utt_tier_correspondences = Vividict()
tbx_utt_tier_correspondences['Chintang']['comm'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['Comment'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['comment'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['context'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['cxt'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['ELANBegin'] = 'starts_at'
tbx_utt_tier_correspondences['Chintang']['ELANEnd'] = 'ends_at'
tbx_utt_tier_correspondences['Chintang']['ELANParticipant'] = 'speaker_id'
tbx_utt_tier_correspondences['Chintang']['eng'] = 'english'
tbx_utt_tier_correspondences['Chintang']['eth'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['EUDICOp'] = 'speaker_id'
tbx_utt_tier_correspondences['Chintang']['EUDICOt0'] = 'starts_at'
tbx_utt_tier_correspondences['Chintang']['EUDICOt1'] = 'ends_at'
tbx_utt_tier_correspondences['Chintang']['gram'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['nep'] = 'nepali'
tbx_utt_tier_correspondences['Chintang']['tx'] = 'phonetic'
tbx_utt_tier_correspondences['Indonesian']['begin'] = 'starts_at'
tbx_utt_tier_correspondences['Indonesian']['ft'] = 'english'
tbx_utt_tier_correspondences['Indonesian']['nt'] = 'comments'
tbx_utt_tier_correspondences['Indonesian']['pho'] = 'phonetic'
tbx_utt_tier_correspondences['Indonesian']['sp'] = 'speaker_id'
tbx_utt_tier_correspondences['Russian']['act'] = 'comments'
tbx_utt_tier_correspondences['Russian']['add'] = 'addressee'
tbx_utt_tier_correspondences['Russian']['com'] = 'comments'
tbx_utt_tier_correspondences['Russian']['ct'] = 'comments'
tbx_utt_tier_correspondences['Russian']['ELANBegin'] = 'starts_at'
tbx_utt_tier_correspondences['Russian']['ELANEnd'] = 'ends_at'
tbx_utt_tier_correspondences['Russian']['ERR'] = 'comments'
tbx_utt_tier_correspondences['Russian']['err'] = 'comments'
tbx_utt_tier_correspondences['Russian']['EUDICOp'] = 'speaker_id'
tbx_utt_tier_correspondences['Russian']['ph'] = 'phonetic'
tbx_utt_tier_correspondences['Russian']['PHO'] = 'phonetic'
tbx_utt_tier_correspondences['Russian']['pho'] = 'phonetic'
tbx_utt_tier_correspondences['Russian']['sit'] = 'comments'

# correspondences between Toolbox word-level tiers and JSON
tbx_word_tier_correspondences = Vividict()
tbx_word_tier_correspondences['Chintang']['gw'] = 'full_word'
tbx_word_tier_correspondences['Indonesian']['tx'] = 'full_word'
tbx_word_tier_correspondences['Russian']['text'] = 'full_word'

# correspondences between Toolbox morpheme-level tiers and JSON
tbx_mor_tier_correspondences = Vividict()
tbx_mor_tier_correspondences['Chintang']['mgl'] = 'glosses_target'
tbx_mor_tier_correspondences['Chintang']['mph'] = 'segments_target'
tbx_mor_tier_correspondences['Chintang']['ps'] = 'pos_target'
tbx_mor_tier_correspondences['Indonesian']['ge'] = 'glosses_target'
tbx_mor_tier_correspondences['Indonesian']['mb'] = 'segments_target'
tbx_mor_tier_correspondences['Russian']['lem'] = 'segments' # Actually there are no segmentations in the Russian corpus, so the levels word and morpheme cannot be separated. However, for consistency across corpora it's best to treat the elements on this tier and on \mor as morphemes (because only morphemes can have glosses). The corresponding "word" tier is \text. 
tbx_mor_tier_correspondences['Russian']['mor'] = 'glosses'


#################
### Functions ###
#################

# TODO move correspondence dics to separate file?

# get all the text contained in an XML tag. This is useful for mixed elements of the form <t1>a<t2>b</t2>c<t1>
def content(tag):
    return tag.text + ''.join(ET.tostring(e) for e in tag)

# create a new key/value pair in a dictionary or concatenate an additional value if the key already exists
def creadd(location, key, value):
    if key not in location.keys():
        location[key] = value
    else:
        location[key] += '; ' + value
    
# format-specific parsing is done by more specific functions called by this one
def parse_corpus(corpus_name, corpus_dir, corpus_format):
    
    # structured corpus
    global corpus
    corpus = Vividict()
    # descriptive statistics
    global stats
    stats = collections.defaultdict()
    stats['xml'] = collections.defaultdict()
    
    format_dic = {
        'XML' : {'regex' : re.compile('.*\.xml$', re.IGNORECASE), 'function' : parse_xml},
        'CHAT' : {'regex' : re.compile('.*\.(chat?)$', re.IGNORECASE), 'function' : parse_chat},
        'Toolbox' : {'regex' : re.compile('.*\.(tbx?|txt)$', re.IGNORECASE), 'function' : parse_toolbox},
    }
    
    # check input
    if not format_dic[corpus_format]:
        print('Format "' + corpus_format + '" for corpus ' + corpus_name + ' does not exist; skipping this corpus')
    if not os.path.exists(corpus_dir):
        print('Path "' + corpus_dir + '" for corpus ' + corpus_name + ' does not exist; skipping this corpus')
    
    # go through all files in corpus directory
    for root, subs, files in os.walk(corpus_dir):
                        
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as file:
                
                # check format of present file and parse as appropriate
                if not format_dic[corpus_format]['regex'].match(file.name):
                    print('file "' + file.name + '" is in unexpected format (should be ' + corpus_format + ') - skipping it')                
                else:
                    print('parsing ' + file.name)
                    format_dic[corpus_format]['function'](file.name, corpus_name)

    # # print descriptive stats
    # for tag in sorted(stats['xml'], key = lambda x: (stats['xml'][x]['freq']), reverse=True):
    #     print 'tag: ' + tag + ' (' + str(stats['xml'][tag]['freq']) + ')'
    #     for attrib in sorted(stats['xml'][tag]['attribs'], key = lambda x: stats['xml'][tag]['attribs'][x]['freq'], reverse=True):
    #         print '\t attribute: ' + attrib + ' (' + str(stats['xml'][tag]['attribs'][attrib]['freq']) + ')'
    #         for value in sorted(stats['xml'][tag]['attribs'][attrib]['values'], key = stats['xml'][tag]['attribs'][attrib]['values'].get, reverse=True):
    #             print '\t\t value: ' + value + ' (' + str(stats['xml'][tag]['attribs'][attrib]['values'][value]) + ')'
                                            
    return corpus
# EOF parse_corpus

# parse an open XML file
def parse_xml(file_name, corpus_name):
        
    # parse XML tree
    tree = ET.parse(file_name)
    root = tree.getroot()
    # get ID of present file
    text_id = root.attrib['Id']

    # walk and clean XML tree for an overview
    for elem in root.iter():
        # remove prefixed namespaces
        elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
        tag = elem.tag
        attrib = elem.attrib

        # collect and count tags, attributes, and values in a nested structure:
        # {'w', 160, {'type', 50, {'untranscribed', 40}}}
        if not tag in stats['xml']:
            stats['xml'][tag] = {}
            stats['xml'][tag]['freq'] = 0
            stats['xml'][tag]['attribs'] = collections.defaultdict()
        stats['xml'][tag]['freq'] += 1
        for key in list(attrib.keys()):
            if not key in stats['xml'][tag]['attribs']:
                stats['xml'][tag]['attribs'][key] = {}
                stats['xml'][tag]['attribs'][key]['freq'] = 0
                stats['xml'][tag]['attribs'][key]['values'] = collections.Counter()
            stats['xml'][tag]['attribs'][key]['freq'] += 1
            stats['xml'][tag]['attribs'][key]['values'][attrib[key]] += 1

    # now translate XML tree to JSON target structure
    
    # get participants and their IDs/names
    # participants = {}
    # for p in root.findall('.//participant'):
    #     if 'name' in p.attrib:
    #         participants[p.attrib['id']] = p.attrib['name']
    #     else:
    #         print('name missing for participant in', file_name)

    # get all utterances
    for u in root.findall('.//u'):

        # utterance index is uID minus '^u'
        utterance_index = re.sub('^\D+', '', u.attrib['uID'])
        utterance_index = int(utterance_index)

        # speaker id and name for utterance
        speaker_id = u.attrib['who']
        corpus[text_id][utterance_index]['speaker_id'] = speaker_id
        # if speaker_id in participants:
        #     corpus[text_id][utterance_index]['speaker_name'] = participants[speaker_id]

        # various optional tags under <u>
        # sentence type
        sentence_type = u.find('t')
        if sentence_type is not None:
            sentence_type_JSON = t_correspondences[sentence_type.attrib['type']]
            corpus[text_id][utterance_index]['sentence_type'] = sentence_type_JSON
        # check for empty utterances, add warning
        if u.find('.//w') is None:
            creadd(corpus[text_id][utterance_index], 'warnings', 'empty utterance')
            # in the Japanese corpora there is a special subtype of empty utterance containing the event tag <e> (for laughing, coughing etc.) -> sentence type
            if u.find('e'): 
                corpus[text_id][utterance_index]['sentence_type'] = 'action'
        
        # time stamps
        time_stamp = u.find('media')
        if time_stamp is not None:
            corpus[text_id][utterance_index]['starts_at'] = time_stamp.attrib['start']
            corpus[text_id][utterance_index]['ends_at'] = time_stamp.attrib['end']
                
        # words
        # first resolve special types of transcriptions
        
        # omissions: ignore them altogether. Omitted words can presently only be removed directly under <w> because ElementTree doesn't give references to parents (i.e. u.findall('.//w') is no good because the parent from which <w> should be dropped is not known). This should be okay, though, since in all XML corpora omissions always occur directly under <u>. 
        for w in u.findall('w'):
            if 'type' in w.attrib and w.attrib['type'] == 'omission':
                u.remove(w)
        
        # simple string replacements
        for w in u.findall('.//w'):
            # where the orthography tier is missing in Cree, <w> is not empty but contains 'missingortho' -> remove this
            if w.text == 'missingortho': 
                w.text = ''
            # CHAT www, xxx, yyy all have an attribute "untranscribed" in XML; unify text to '???'
            if 'untranscribed' in w.attrib:
                w.text = '???'
            # only in Cree: morpheme boundaries in <w> are indicated by '_' -> remove these, segments are also given in the morphology tiers. Other corpora can have '_' in <w>, too, but there it's meaningful (e.g. for concatenating the parts of a book title treated as a single word), so only check Cree!
            # TODO morphemes in Cree <w> should be used for morpheme shape, they correspond to dic entries and are invariable!
            if corpus_name == 'Cree' and w.text:
                w.text = re.sub('_', '', w.text)
            # In ElementTree, w.text only stores the text immediately following <w>. In <w>ha<p type="drawl"/>i</w>, only 'ha' is stored as the text of <w> whereas 'i' is stored as the tail of <p>. Tags of this type are: <p> ('prosody marker'), <ca-element> ('pitch marker'), and <wk> ('word combination', marks boundaries between the elements of compounds)
            for path in ('.//p', './/ca-element', './/wk'):
                for t in w.findall(path):
                    if t.tail is not None:
                        if w.text is None:
                            w.text = t.tail
                        else:
                            w.text += t.tail
        # EOF string replacements
                
        # group tags <g> in Japanese corpora surround groups of problematic words (transcription insecure, no glosses, ...)
        for g in u.findall('.//g'):
            words = g.findall('.//w')
            # repetitions, e.g. <g><w>shoo</w><w>boo</w><r times="3"></g>: insert as many <w> groups as indicated by attrib "times" of <r>, minus 1 (-> example goes to "shoo boo shoo boo shoo boo"), attribute 'glossed' to 'no'
            # TODO it would be nicer to repeat the glosses, too, but this requires a special pattern, e.g. attribute 'glossed' to 'copy'??
            repetitions = g.find('r')
            if repetitions is not None:
                for i in range(0, int(repetitions.attrib['times'])-1):
                    for w in words:
                        new_elem = ET.SubElement(g, 'w')
                        new_elem.text = w.text
                        new_elem.attrib['glossed'] = 'no'
            # retracings, e.g. <g><w formType="UNIBET">shou</w><w formType="UNIBET">shou</w><k type="retracing"/></g>: set attribute 'glossed' to 'no'
            retracings = g.find('k[@type="retracing"]')
            retracings_wc = g.find('k[@type="retracing with correction"]')
            if (retracings is not None) or (retracings_wc is not None):
                for w in words: 
                    w.attrib['glossed'] = 'no'
            # guessed transcriptions: add warning
            guesses = g.find('k[@type="buest guess"]')
            if guesses is not None:
                for w in words:
                    w.attrib['transcribed'] = 'insecure'
            
        # EOF group tags
                                    
        # transcriptions featuring a contrast between actual and target pronunciation: go through words, create an attribute "target" (initially identical to its text), and set it as appropriate. "target" is taken up later again when all content is written to the corpus dic. 
        for w in u.findall('.//w'):
            
            # Note that in ElementTree, w.text only stores the text immediately following <w>. In <w>al<shortening>pha</shortening>bet</w>, only 'al' is stored as the text of <w> whereas bet' is stored as the tail of <shortening>. Therefore, actual and target pronunciation have to be assembled step by step in most cases. 
            if w.text is None:
                w.text = ''
            w_actual = w.text
            w_target = w.text

            # fragments: actual pronunciation remains, target pronunciation is '???' as with untranscribed words. No glosses. This may occasionally be overwritten by a <replacement> further down.
            if 'type' in w.attrib and w.attrib['type'] == 'fragment':
                w.attrib['target'] = '???'
                w.attrib['glossed'] = 'no'
                continue
            
            # shortenings, e.g. <g><w>wo<shortening>rd</shortening>s</w></g>: 'wos' = actual pronunciation, 'words' = target pronunciation
            # shortenings have to be processed before replacements because a target string with no shortenings may still be classified as a replaced form 
            for s in w.findall('shortening'):
                if s.text is not None:
                    w_target += s.text
                if s.tail is not None:
                    w_target += s.tail
                    w_actual += s.tail
                w.remove(s)
            w.text = w_actual
            w.attrib['target'] = w_target
        # EOF actual vs target    
            
        # replacements, e.g. <g><w>burred<replacement><w>word</w></replacement></w></g>
        # these require an additional loop over <w> in <u> because there may be shortenings within replacements
        words = u.findall('.//w')
        for i in range(0, len(words)):
            r = words[i].find('replacement')
            if r is not None:
                rep_words = r.findall('w')
                words[i].attrib['target'] = rep_words[0].attrib['target']
                # a single actual word may be replaced by several target words. In this case it is necessary to insert empty actual words corresponding to all but the first target word. 
                if len(rep_words) > 1:
                    for j in range(1, len(rep_words)):
                        w = ET.Element('w')
                        w.text = ''
                        w.attrib['target'] = rep_words[j].attrib['target']
                        u.insert(i+1, w)
                        
                # w.attrib['target'] = '_'.join(rep_w.attrib['target'] for rep_w in r.findall('w'))
                words[i].remove(r)

                # example for shortening within complex replacement in Japanese MiiPro (aprm19990722.u287), processing step by step:
                # (1) initial XML string
                #   <w>kitenee<replacement><w>kite</w><w><shortening>i</shortening>nai</w></replacement></w>
                # (2) add targets to all <w>
                #   <w target="kitenee">kitenee<replacement><w target="kite">kite</w><w target="nai"><shortening>i</shortening>nai</w></replacement></w>
                # (3) reset target for shortening  
                #   <w target="kitenee">kitenee<replacement><w target="kite">kite</w><w target="inai"><shortening>i</shortening>nai</w></replacement></w>
                # (4) remove shortening tag
                #   <w target="kitenee">kitenee<replacement><w target="kite">kite</w><w target="inai">nai</w></replacement></w>
                # (5) reset target for w to replacement
                #   <w target="kite">kitenee<replacement><w target="kite">kite</w><w target="inai">nai</w></replacement></w>
                # (6) insert new empty word with target = second element of replacement
                #   <w target="kite">kitenee<replacement><w target="kite">kite</w><w target="inai">nai</w></replacement></w><w target="inai"/>
                # (7) remove replacement tag
                #   <w target="kite">kitenee</w><w target="inai"/>
        
        # EOF replacements
                
        # remember number of (glossed!) words to check alignment later
        words = u.findall('.//w')
        unglossed_words = u.findall('.//w[@glossed="no"]')
        corpus[text_id][utterance_index]['length_in_words'] = len(words) - len(unglossed_words)
        # print(file_name, utterance_index, ":", len(words), "words;", len(unglossed_words), "unglossed words; so length should be", corpus[text_id][utterance_index]['length_in_words'])
        
        # write words to corpus dic
        word_index = 0
        for w in words:
            corpus[text_id][utterance_index]['words'][word_index]['full_word'] = w.text
            corpus[text_id][utterance_index]['words'][word_index]['full_word_target'] = w.attrib['target']
            # pass down warnings
            if 'glossed' in w.attrib and w.attrib['glossed'] == 'no':
                creadd(corpus[text_id][utterance_index]['words'][word_index], 'warnings', 'not glossed')
            if 'transcribed' in w.attrib and w.attrib['transcribed'] == 'insecure':
                creadd(corpus[text_id][utterance_index]['words'][word_index], 'warnings', 'transcription insecure')
            word_index += 1
                        
        # standard dependent tiers
        for dependent_tier in xml_dep_correspondences:
            tier = u.find("a[@type='" + dependent_tier + "']")
            if tier is not None:
                tier_name_JSON = xml_dep_correspondences[dependent_tier]
                creadd(corpus[text_id][utterance_index], tier_name_JSON, tier.text)
                        
        # extended dependent tiers
        for extension in xml_ext_correspondences:
            tier = u.find("a[@type='extension'][@flavor=']" + extension + "']")
            if tier is not None: 
                tier_name_JSON = xml_ext_correspondences[extension]
                corpus[text_id][utterance_index][tier_name_JSON] = tier.text
        
        # corpus-specific stuff
        if corpus_name == 'Cree':
                                    
            # Cree has phonetic tags <actual> and <model>, both of which contain phonological words <pw> consisting of special characters <ss> and phones <ph>
            # Keep the words but concatenate the phones; add single string to corpus directly under utterance level
            for variant in ('actual', 'model'):
                tier_name_JSON = xml_other_correspondences[variant]
                block = u.find('.//' + variant)
                if block is not None:
                    words = {}
                    for w in block.findall('pw'):
                        word_concatenated = ''
                        for child in w:
                            if child.tag == 'ph':
                                word_concatenated += child.text
                            elif child.tag == 'ss' and child.attrib['type'] == '1':
                                word_concatenated += 'ʼ'
                            elif child.tag == 'ss' and child.attrib['type'] != '1':
                                print('unknown Cree type', child.attrib['type'], '- update export script!')
                            elif child.tag != 'ss':
                                print('unknown Cree phonetic element', child.tag, '- update export script!')
                        if not corpus[text_id][utterance_index][tier_name_JSON]:
                            corpus[text_id][utterance_index][tier_name_JSON] = word_concatenated
                        else:
                            corpus[text_id][utterance_index][tier_name_JSON] = corpus[text_id][utterance_index][tier_name_JSON] + ' ' + word_concatenated
                        
            # Cree has four different morphology tiers that may be aligned with words <w> and require parsing
            # In order to compare the morphology tiers (e.g. for alignment), they have to be stored in a temporary Vividict before they can be added to the corpus dic
            morphology = Vividict()
               
            # split morphology tiers into words
            any_morphology = False
            for morph_tier in ('mortyp', 'mormea', 'tarmor', 'actmor'):
                tier = u.find("a[@type='extension'][@flavor='" + morph_tier + "']")
                if tier is not None:
                    any_morphology = True
                    tier_name_JSON = xml_other_correspondences[morph_tier]
                    
                    # edit tier syntax
                    # first remove spaces within glosses so that only word boundary markers remain
                    tier.text = re.sub('\\s+(&gt;|>)\\s+', '>', tier.text)
                    # remove square brackets at edges of any of these tiers, they are semantically redundant
                    tier.text = re.sub('^\[|\]$', '', tier.text)
                    # apparently no difference between "=" and "-" as morpheme separators, so use "=" for all
                    tier.text = re.sub('-', '=', tier.text)
                    # replace untranscribed and/or unglossed words by standard formalisms
                    tier.text = re.sub('#|%%%|\*|(?<=\\s)\?(?=\\s)', '???', tier.text)
                    # delete brackets in "mortyp" and uppercase content to emphasise its abstract nature
                    if morph_tier == 'mortyp':
                        tier.text = re.sub('\(([^\)]+)\)', '\\1'.upper(), tier.text)
                    # delete brackets in "tarmor" and "actmor"
                    if morph_tier == 'tarmor' or morph_tier == 'actmor':
                        tier.text = re.sub('[\(\)]', '', tier.text)
                    # replace "," (separator between gloss and subgloss) by "."
                    tier.text = re.sub(',', '.', tier.text)

                    # split into words
                    words = re.split('\\s+', tier.text)
                    
                    # check alignment with words that were found in <w> 
                    if len(words) != corpus[text_id][utterance_index]['length_in_words']:
                        print('alignment problem in ' + file_name + ', utterance ' + str(utterance_index) + ': general word tier <w> has ' 
                            + str(corpus[text_id][utterance_index]['length_in_words']) + ' words vs ' + str(len(words)) + ' in "' + morph_tier + '" (= ' 
                            + tier_name_JSON + ')')
                        creadd(corpus[text_id][utterance_index], 'warnings', 'broken alignment full_word : ' + tier_name_JSON)
                                            
                    # split words into morphemes, add to Vividict
                    word_index = 0
                    for w in words:
                        morpheme_index = 0
                        morphemes = re.split('=', w)
                        for m in morphemes:
                            morphology[morph_tier][word_index][morpheme_index] = m
                            morpheme_index += 1
                        word_index += 1                    
                    
            # if there is no morphology, add warning to complete utterance
            if any_morphology == False:
                creadd(corpus[text_id][utterance_index], 'warnings', 'not glossed')
            
            
            # after analysing all four morphology tiers, go through Vividict to check alignment and add everything to corpus dic
            # first do words
            max_length_words = max(len(morphology['mortyp']), len(morphology['mormea']), len(morphology['tarmor']), len(morphology['actmor']))
            for morph_tier in ('mortyp', 'mormea', 'tarmor', 'actmor'):
                tier_name_JSON = xml_other_correspondences[morph_tier]
                if len(morphology[morph_tier]) != max_length_words and len(morphology[morph_tier]) != 0:
                    print('alignment problem in ' + file_name + ', utterance ' + str(utterance_index) + ': there should be ' 
                        + str(max_length_words) + ' words in all tiers, but ' + morph_tier + ' (=' + tier_name_JSON + ') has only ' 
                        + str(len(morphology[morph_tier]))) 
                    creadd(corpus[text_id][utterance_index], 'warnings', 'broken alignment between morphology tiers - word numbers don\'t match. Check' + tier_name_JSON)
                
            # go through words
            for word_index in range(0, max_length_words):
                max_length_morphemes = max(len(morphology['mortyp'][word_index]), len(morphology['mormea'][word_index]), len(morphology['tarmor'][word_index]), len(morphology['actmor'][word_index]))
                for morph_tier in ('mortyp', 'mormea', 'tarmor', 'actmor'):
                    tier_name_JSON = xml_other_correspondences[morph_tier]
                    # check morpheme alignment
                    if len(morphology[morph_tier][word_index]) != max_length_morphemes and len(morphology[morph_tier][word_index]) != 0:
                        print('alignment problem in ' + file_name + ', utterance ' + str(utterance_index) + ', word ' + str(word_index) + ': there should be ' 
                            + str(max_length_morphemes) + ' morphemes in all tiers, but ' + morph_tier + ' (=' + tier_name_JSON + ') has only ' 
                            + str(len(morphology[morph_tier][word_index])) + ' for this word')
                        creadd(corpus[text_id][utterance_index], 'warnings', 'broken alignment between morphology tiers - morpheme numbers don\'t match. Check' + tier_name_JSON)    
                    # add morphemes to corpus dic
                    for morpheme_index in range(0, max_length_morphemes):
                        m = morphology[morph_tier][word_index][morpheme_index]
                        if m:
                            # check for "?" attached to gloss; replace by warning that gloss is insecure
                            if re.search('\?', morphology[morph_tier][word_index][morpheme_index]):
                                 creadd(corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index], 'warnings', 'gloss insecure for tier' + tier_name_JSON)
                            m = re.sub('\?', '', m)
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = m
        # EOF Cree                    
                                                   
        elif corpus_name == 'Japanese_MiiPro':
            # TODO quotations are marked by <quotation type="begin"></quotation> and <quotation type="end"></quotation>. The complete group is represented in the morphology tier trn by n|quote, so all words in the group except the first should have an attribute 'not glossed', similar to fragments, replacements, and retracings. It will be difficult to include these because the quoted elements are hard to catch in XPath. 
                        
            # parse the morphology tier trn
            morphology = u.find("a[@type='extension'][@flavor='trn']")
            if morphology is not None:
                # split trn tier into words, reset counters to 0
                words = re.split('\\s+', morphology.text)
                word_index = 0
                words_in_trn = 0
                                
                for w in words:
                    # skip "words" that contain no '|' (= punctuation, e.g. '.'); 
                    if not re.search('\\|', w):
                        continue
                    # ignore "tags" tag|„ and tag|‡, they are not words but mark syntactic stuff on a higher level
                    if re.search('^tag\\|', w):
                        continue
                        
                    # only now count up words_in_trn
                    words_in_trn += 1
                        
                    # some words are not glossed - these got a warning 'not glossed' further above. Ignore them here, i.e. count one up
                    while 'warnings' in corpus[text_id][utterance_index]['words'][word_index].keys() and re.search(corpus[text_id][utterance_index]['words'][word_index]['warnings'], 'not glossed'):
                        word_index += 1
                    
                    # set morpheme counter
                    morpheme_index = 0
                    
                    # first cut off prefix, it's always on the left edge of the complete word. There are no words with more than 1 prefix in MiiPro. 
                    prefix = ''
                    check_pfx = re.search('^(.+#)', w)
                    if check_pfx:
                        prefix = check_pfx.group(1) 
                        w = w.lstrip(prefix)
                        prefix = prefix.replace('#', '')
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['segments_target'] = prefix
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['glosses_target'] = '???'
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['pos_target'] = 'pfx'
                                                
                        morpheme_index += 1
                        
                    # cut off "supertags" prefixed to compounds, e.g. the 'num|' in num|+num|kyuu+num|juu. There are no words with more than 1 supertag. 
                    # note that the dedicated tag for compounds, <wk>, is considered irrelevant for us and is removed further above. It is used rarely (7 times) and inconsistently in MiiPro. 
                    check_compound = re.search('^[^\\+]+\\+(.*)', w)
                    if check_compound:
                        w = check_compound.group(1)
                    
                    # get stem gloss from the right edge of the complete word. There are no words with more than 1 stem gloss. 
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
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['segments_target'] = stem
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['glosses_target'] = stem_gloss
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['pos_target'] = stem_pos
                        morpheme_index += 1
                        
                        if suffix_string:
                            # drop first hyphen in suffix string so split() doesn't produce empty elements
                            suffix_string = suffix_string.lstrip("-")
                            for suffix_gloss in suffix_string.split('-'):
                                # most suffixes don't have form glosses in MiiPro, but sometimes blocks of the type IMP:te are found, in which case IMP is the suffix gloss and -te is the suffix form. Only exception is [A-Z]:contr, which is not a stem gloss but indicates contractions.
                                suffix_form = '???'
                                check_suffix = re.search('^([A-Z]+):(\w+)$', suffix_gloss)
                                if check_suffix and check_suffix.group(2) != 'contr':
                                    suffix_gloss = check_suffix.group(1)
                                    suffix_form = check_suffix.group(2)
                                
                                corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['segments_target'] = suffix_form
                                corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['glosses_target'] = suffix_gloss
                                corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['pos_target'] = 'sfx'
                                morpheme_index += 1
                    
                    # count up words
                    word_index += 1
            
                # check alignment with words that were found in <w>. This can only be done now because before "trn" contained punctuation that wasn't present in <w>.
                # note: alignment on morpheme-level doesn't have to be checked at all for MiiPro because the segment and gloss tiers are not separate
                if words_in_trn != corpus[text_id][utterance_index]['length_in_words']:
                    print('alignment problem in ' + file_name + ', utterance ' + str(utterance_index) + ': general word tier <w> has ' 
                        + str(corpus[text_id][utterance_index]['length_in_words']) + ' words vs ' + str(words_in_trn) + ' in "trn" (= morphology)')
                    creadd(corpus[text_id][utterance_index], 'warnings', 'broken alignment full_word : segments/glosses')

            # if there is no morphology, add warning to complete utterance
            elif morphology is None:
                creadd(corpus[text_id][utterance_index], 'warnings', 'not glossed')
                
        # EOF Japanese MiiPro        
            
        elif corpus_name == 'Japanese_Miyata':
            
            # Japanese Miyata has the standard tier called "coding", which seems to contain annotations for information structure in this corpus
            tier = u.find("a[@type='coding']")
            if tier is not None: 
                corpus[text_id][utterance_index]['information_structure'] = tier.text
            
            # Miyata is the only corpus with morphology coded in explicit XML style, so at least alignment doesn't have to be checked
            # note that there are two tags for compounds. <wk> (between <u> and <w>) is considered irrelevant for us and therefore removed further above in the general part. It is used rarely (21 times) and inconsistently. The other one, <mwc> (between <mor> and <mw> is part of the morphology subtree and is parsed here. 
            word_index = 0
            for w in u.findall('.//w'):
                morphology = w.find('mor')
                if morphology is not None:
                    morpheme_index = 0
                    compound_gloss = ''
                    
                    # check whether there are compound elements. There can only ever be one <mwc> per <mor>. <mwc> have their own POS tags, but these are ignored here.
                    compound = morphology.find('mwc')
                    if compound is not None:
                        # all stems in the compound except the first get the prefix "=" as a separator. 
                        mw = compound.findall('mw')
                        for i in range(1, len(mw)):
                            # every morphological word has exactly one stem
                            stem = mw[i].find('stem')
                            stem.text = '=' + stem.text
                        # if there are any prefixes on the compound, add them to the corpus dic directly
                        # compounds never carry suffixes in Miyata XML
                        for p in compound.findall('mpfx'):
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['segments_target'] = p.text
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['glosses_target'] = '???'
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['pos_target'] = 'pfx'
                            
                            morpheme_index += 1
                        # in compounds the meaning tag <menx> applies to the whole compound, but we want meanings for words -> remember meaning
                        menx = morphology.find('menx')
                        if menx is not None:
                            compound_gloss = menx.text
                    
                    # go through morphological words
                    for mw in morphology.findall('mw'):
                        
                        # prefixes under <mw>
                        for p in mw.findall('mpfx'):
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['segments_target'] = p.text
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['glosses_target'] = '???'
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['pos_target'] = 'pfx'
                            morpheme_index += 1
                        
                        # stem (exactly one in every <mw>) with gloss and part of speech
                        stemtag = mw.find('stem')
                        stem = stemtag.text
                        # if <mw> is part of a compound, the meaning tag <menx> refers to the compound as a whole -> repeat it for all <mw> 
                        # otherwise <menx> refers to the meaning of the stem
                        stem_gloss = ''
                        if compound_gloss: 
                            stem_gloss = compound_gloss
                        else: 
                            menx = morphology.find('menx')
                            if menx is None:
                                stem_gloss = '???'
                            else:    
                                stem_gloss = menx.text
                        # part of speech
                        pos = mw.find('pos')
                        main_pos = pos.find('c')
                        stem_pos = main_pos.text
                        for sub_pos in pos.findall('s'): 
                            stem_pos = stem_pos + '.' + sub_pos.text
                        # add to corpus dic
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['segments_target'] = stem
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['glosses_target'] = stem_gloss
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['pos_target'] = stem_pos
                        
                        morpheme_index += 1
                                                    
                        # suffixes (in a wide sense)
                        for s in mw.findall('mk'):
                            # add to corpus dic
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['segments_target'] = '???'
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['glosses_target'] = s.text
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['pos_target'] = s.attrib['type']
                            morpheme_index += 1                                                        
       
                        # count up words
                        word_index += 1
                # if there is no morphology, add warning to present word and count up
                elif morphology is None:
                    creadd(corpus[text_id][utterance_index]['words'][word_index], 'warnings', 'not glossed')
                    word_index += 1

        # EOF Japanese Miyata                
                        
        elif corpus_name == 'Sesotho':      
            
            # Sesotho has two morphology tiers, "target gloss" (= segments) and "coding" (= glosses and POS). Parse and align.             
            # Segments. The Sesotho segment tier doesn't make a clear distinction between affixes and stems, so its elements can't be added to the corpus dic until they have been compared with the glosses. Store them in a temporary Vividict().
            segment_tier = u.find("a[@type='target gloss']")
            segments = Vividict()
            if segment_tier is not None:                
                # split into words
                word_index = 0
                segment_words = re.split('\\s+', segment_tier.text)
                for w in segment_words:
                    # Check brackets. In Sesotho, these are only used to mark contractions of the verb 'go' which are conventional in both child and adult speech. The form of 'go' is given in brackets from the first to the last morpheme, is completely covert, and does not correspond to an element in <w>, so drop it altogether. The following, partially bracketed INF (if-) has an effect on the contracted surface form, so only remove the brackets but keep the gloss.
                    if re.search('^\(.*\)$', w):
                        continue
                    else:
                        w = re.sub('[\(\)]', '', w)
                    
                    # split into morphemes
                    morpheme_index = 0
                    for m in re.split('\\-', w):
                        segments[word_index][morpheme_index] = m
                        morpheme_index += 1
                    word_index += 1
                        
            # Glosses and POS
            gloss_tier = u.find("a[@type='coding']")    
            if gloss_tier is not None: 
                word_index = 0
                # first remove spaces in noun class brackets
                gloss_tier.text = re.sub('\\s+,\\s+', ',', gloss_tier.text)
                # replace / as noun class separator by | so it can't be confused with / as a morpheme separator
                gloss_tier.text = re.sub('(\d+a?)\\/(\d+a?)', '\\1|\\2', gloss_tier.text)
                
                # the remaining spaces indicate word boundaries -> split
                gloss_words = re.split('\\s+', gloss_tier.text)
                
                # check alignment between segments and glosses on word level
                if len(gloss_words) != len(segment_words):
                    print('alignment problem in ' + file_name + ', utterance ' + str(utterance_index) + ': tier "target gloss" (= segments_target) has ' + 
                        str(len(segments)) + ' words vs. ' + str(len(gloss_words)) + ' in "coding" (= glosses_target)')
                    creadd(corpus[text_id][utterance_index], 'warnings', 'broken alignment segments_target : glosses_target')
                    
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
                        w = re.sub('\(([a-z]\\S+)\)', '\\1', w)
                    
                    # split into morphemes
                    morpheme_index = 0
                    passed_stem = False
                    glosses = re.split('[\\-]', w)
                    
                    # check alignment between segments and glosses on morpheme level
                    if len(glosses) != len(segments[word_index]):
                        print('alignment problem in' + file_name + ', utterance ' + str(utterance_index) + ', word ' + str(word_index) +
                            ': tier "target gloss" (= segments_target) has ' + str(len(segments[word_index])) + ' morphemes vs. ' + str(len(glosses)) + 
                            ' in "coding" (= glosses_target)')
                        creadd(corpus[text_id][utterance_index]['words'][word_index], 'warnings', 'broken alignment segments_target : glosses_target')
                        
                    for gloss in glosses:
                        # replace special characters
                        # n^ prefixed to all noun class glosses: delete
                        gloss = re.sub('[nN]\^(?=\\d)', '', gloss)
                        # n^ prefixed to all proper names: replace by 'a_'
                        gloss = re.sub('[nN]\^(game|name|place|song)', 'a_\\1', gloss)
                        # t^ and m^ prefixed to affixes: replace by more explicit labels, also replace '_' by more standard '.'
                        gloss = re.sub('t\^(p|f\\d|np)_', 'temp.\\1.', gloss)
                        gloss = re.sub('t\^', 'temp.', gloss)
                        gloss = re.sub('m\^', 'mood.', gloss)
                        # replace noun class numbers by more standard Roman numbers; exception are [12][sp] (= SAP) and f\d (= FUT)
                        num_dic = {'0' : '0', '1' : 'I', '2' : 'II', '3' : 'III', '4' : 'IV', '5' : 'V', '6' : 'VI', '7' : 'VII', '8' : 'VIII', '9' : 'IX', 
                            '10' : 'X', '11' : 'XI', '12' : 'XII', '13' : 'XIII', '14' : 'XIV', '15' : 'XV', '16' : 'XVI', '17' : 'XVII', '18' : 'XVIII', 
                            '19' : 'XIX', '20' : 'XX', '21' : 'XI', '22' : 'XII'}
                        reverse_num_dic = {'I' : '1', 'II' : '2', 'III' : '3', 'IV' : '4', 'V' : '5'}
                        for n in re.findall('((?<!f)\\d+(?![sp]))', gloss):
                            gloss = re.sub(n, num_dic[n], gloss)
                        
                        # check whether present element is the stem; if no, set POS to prefix/suffix
                        pos = ''
                        if len(glosses)==1 or re.search('(n|v|id)\^|\(\d', gloss) or re.match('(aj$|nm$|ps\d+)', gloss):
                            passed_stem = True
                        elif passed_stem == False:
                            pos = 'pfx'
                        elif passed_stem == True:
                            pos = 'sfx'
                        
                        # get remaining POS and remove indicators and other clutter in the morpheme string
                        pos_dic = {'aj' : 'adj', 'av' : 'adv', 'cd' : 'ptcl', 'cj' : 'conj', 'cm' : 'ptcl', 'd' : 'dem', 
                            'ht' : 'ptcl', 'ij' : 'intj', 'loc' : 'ptcl', 'lr' : 'rel', 'ng' : 'ptcl', 'nm' : 'num', 'obr' : 'rel',
                            'or' : 'rel', 'pn' : 'pro', 'pr' : 'prep', 'ps' : 'poss', 'q' : 'ptcl',
                            'sr' : 'rel', 'wh' : 'intrg'}
                        gloss_dic = {'cd' : 'COND', 'cm' : 'COMP', 'ht' : 'HORT', 'loc' : 'LOC', 'ng' : 'NEG', 
                            'obr' : 'REL.OBL', 'or' : 'REL.OBJ', 'q' : 'Q', 'rl' : 'REL.LOC', 'sr' : 'REL.SUBJ'}
                        # affixes already have their POS, but replace '_' as concatenator by more standard '.'
                        if pos=='pfx' or pos=='sfx':
                            gloss = re.sub('_', '.', gloss)
                        # verbs have v^, one typo as s^
                        elif re.search('[vs]\^', gloss): 
                            pos = 'v'
                            gloss = re.sub('[vs]\^', '', gloss)
                        # nouns have their class indicated in brackets, proper names start with 'a_' (< earlier 'n^'); some nouns with suppletive possession only have "ps/"
                        elif re.search('\(\\d+', gloss) or re.search('a_[a-z]{2,}', gloss) or re.search('^ps\/', gloss):
                            pos = 'n'
                            gloss = re.sub('^ps(\d+)\/', '\\1.POSS.', gloss)
                            gloss = re.sub('^ps\/', 'POSS.', gloss)
                        # words with nominal concord
                        elif re.search('^(d|lr|obr|or|pn|ps|sr)\d+', gloss):
                            pos_match = re.search('^(d|lr|obr|or|pn|ps|sr)\d+', gloss)
                            old_pos = pos_match.group(1)
                            pos = pos_dic[old_pos]                            
                            gloss = re.sub(old_pos, '', gloss)
                        # various particles, mostly without a precise gloss
                        elif re.search('^(aj|av|cd|cj|cm|ht|ij|loc|lr|ng|nm|obr|or|pr|q|sr|wh)$', gloss):
                            pos = pos_dic[gloss]
                            if gloss in gloss_dic:
                                gloss = gloss_dic[gloss]
                            else:    
                                gloss = '???'
                        # free person markers (rare)
                        elif re.search('^sm\d+[sp]?$', gloss):
                            pos = 'afx.detached'
                            gloss = re.sub('sm', '', gloss)
                        # copula
                        elif re.search('^cp|cp$', gloss):
                            pos = 'cop'
                            gloss = re.sub('cp', 'COP.', gloss)
                        # ideophones
                        elif re.search('id\^', gloss): 
                            pos = 'ideoph'
                            gloss = re.sub('id\^', '', gloss)
                        # punctuation marks
                        elif re.search('^[.!\?]$', gloss):
                            pos = 'punct'
                        # meaningless and unclear words. Note that "xxx" in the Sesotho coding tier is not the same as CHAT "xxx" in the transcription tier - it does not stand for words that could not be transcribed but for words with unclear meaning. 
                        elif gloss == 'word' or gloss == 'xxx':
                            pos = 'none'
                            gloss = '???'
                        else:
                            pos = '???'
                        
                        # now put together segment, gloss, and POS
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['glosses_target'] = gloss
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['pos_target'] = pos                        
                        # if there happen to be more glosses than segments (-> misalignment), the segment indices don't go as far as the gloss indices, so first check
                        if segments[word_index][morpheme_index]: 
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['segments_target'] = segments[word_index][morpheme_index]
                        else: 
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index]['segments_target'] = ""
                        
                        # count up morphemes
                        morpheme_index += 1
                        
                    # count up words
                    word_index += 1
                
                # check alignment between glosses and words that were found in <w>. This can be done only now because glosses contain punctuation (dropped in the end) but <w> doesn't. 
                # alignment between <w> and segments doesn't have to be checked separately because glosses:segments is already checked above and good alignment for both glosses:segments and glosses:<w> entails good alignment for segments:<w>
                if word_index != corpus[text_id][utterance_index]['length_in_words']:
                    print('alignment problem in ' + file_name + ', utterance ' + str(utterance_index) + ': general word tier <w> has ' 
                        + str(corpus[text_id][utterance_index]['length_in_words']) + ' words vs ' + str(word_index) + ' in "coding" (= glosses_target)')
                    creadd(corpus[text_id][utterance_index], 'warnings', 'broken alignment full_word : glosses_target')
            # if there is no morphology, add warning to complete utterance
            elif gloss_tier is None:
                creadd(corpus[text_id][utterance_index], 'warnings', 'not glossed')
        # EOF Sesotho        
    
    # EOF utterance loop
    
# EOF parse_xml

# parse an open Toolbox file
def parse_toolbox(file_name, corpus_name):

    # get session ID from file name
    structure = re.search('^.*\/(.*)\.(txt|tbx?)$', file_name)
    text_id = structure.group(1)
    
    with open(file_name) as file:
        # read file into a single string
        text = file.read()
        # get rid of BOM if present; otherwise Python will treat this like a character under UTF-8
        text = re.sub(u'\ufeff', '', text)
        # get rid of other weird stuff
        text = re.sub('', '', text)
                
        # split by at least two \n to get records (approximating utterances)
        utterances = re.split('\\n{2,}', text)
        
        # go through utterances
        for u in utterances:
            # split by single \n to get tiers
            tiers = re.split('\\n', u)
            
            # store tiers in temporary dic for random access
            record = collections.defaultdict()
            for t in tiers:
                
                # throw away empty tiers and technical tiers
                if re.search('^\\s*$', t) or re.search(r'^\\_', t) or not re.search('\\s', t) or re.search('^@', t):
                    continue                    
                    
                else:
                    # separate field marker and content    
                    structure = re.split('\\s+', t, maxsplit=1)
                    (field_marker, content) = (structure[0], structure[1])
                    field_marker = field_marker.lstrip(r'\\')
                    content = content.rstrip()

                    # edit field markers and contents
                    # Chintang: inconsistent field markers
                    field_marker = re.sub('TOS', 'tos', field_marker)
                    # Russian & Indonesian: garbage imported from CHAT
                    content = re.sub('xxx?|www', '???', content)
                    
                    # then save
                    record[field_marker] = content
            
            # now check tiers in right order, split and/or add to corpus dic
            if record:
                
                utterance_index = ''
                
                # \ref = record marker, extract utterance index. Ignore complete record if marker is missing or invalid. 
                if not 'ref' in record.keys():
                    print(file_name + ': record without record marker detected; last tier was', t)
                    continue
                
                # corpus-specific measures: extract utterance ID; clean tiers BEFORE doing any splits
                
                if corpus_name is 'Chintang':
                    structure = re.search('.*\.(\\d+\.?[a-z]?)$', record['ref'])
                    if structure is not None: utterance_index = structure.group(1)
                # EOF Chintang checks
                
                elif corpus_name is 'Russian':
                    structure = re.search('.*_(\\d+)$', record['ref'])
                    if structure is not None: utterance_index = structure.group(1)
                    
                    # stuff found in \text and \pho
                    for tier in ('text', 'pho'):
                        if tier in record.keys():
                        
                            # delete punctuation, set utterance type
                            match_punctuation = re.search('([\.\?!])$', record[tier])
                            if match_punctuation is not None:
                                corpus[text_id][utterance_index]['sentence_type'] = t_correspondences[match_punctuation.group(1)]
                            record[tier] = re.sub('[‘’\'“”\"\.!,:\+\/]+|(?<=\\s)\?(?=\\s|$)', '', record[tier])
                            record[tier] = re.sub('\\s\-\\s', ' ', record[tier])
                        
                            # insecure transcriptions [?], [=( )?], [xxx]: add warning, delete marker. Note that [xxx] usually replaces a complete utterance and is non-aligned, in contrast to xxx without brackets, which can be counted as a word
                            if re.search('\[(\s*=?\s*\?\s*|\s*xxx\s*)\]', record[tier]):
                                creadd(corpus[text_id][utterance_index], 'warnings', 'transcription insecure')
                                record[tier] = re.sub('\[\s*=?\s*\?\s*\]', '', record[tier])
                    
                    # stuff only found in \text
                    if 'text' in record.keys():  
                        
                        # comments [= ...]: relocate to separate tier. It's important ro re.escape the match so the [] are interpreted literally!
                        for comment, content in re.findall('(\[=\\s+([^\]]{2,})\])', record['text']):
                            record['text'] = re.sub(re.escape(comment), '', record['text'])  
                            if not 'comments' in corpus[text_id][utterance_index]:
                                corpus[text_id][utterance_index]['comments'] = content
                            else:
                                corpus[text_id][utterance_index]['comments'] += '; ' + content
                        # overlaps [...]: remove completely, they are always transcribed twice
                        for overlap in re.findall('\[[a-z][^\]]+\]', record['text']):        
                            record['text'] = re.sub(re.escape(overlap), '', record['text'])
                        # guesses at intended form [=? ...]: this is used rarely (78 times overall), so it's easier to turn it into a comment than to convert it to a full_word_target
                        for target in re.findall('\[=\?\s+[^\]]+\]', record['text']):
                            record['text'] = re.sub(re.escape(target), '', record['text'])
                            if not 'comments' in corpus[text_id][utterance_index]:
                                corpus[text_id][utterance_index]['comments'] = 'intended form might have been "' + target + '"'
                            else:
                                corpus[text_id][utterance_index]['comments'] += '; ' + 'intended form might have been "' + target + '"'
                        # various undocumented markers starting with +, only partially well-formed CHAT, e.g. +//, +., [+]: delete
                        record['text'] = re.sub('\+\S+|\[\s*\+\]|\[\]|\[|\]', '', record['text'])
                        # other undocumented markers: delete
                        record['text'] = re.sub('&lt;', '', record['text'])
                    
                    # stuff only found in \mor
                    if 'mor' in record.keys():
                        record['mor'] = re.sub('<NA: [^>]+>', '', record['mor'])
                
                # EOF Russian checks
                
                elif corpus_name is 'Indonesian':
                    # TODO speaker codes in Indonesian often have code of target child suffixed to them (e.g. CHI -> CHIHIZ). These suffixes are not present in the complete metadata, so remove them!
                    structure = re.search('^(\\d+)$', record['ref'])
                    if structure is not None: utterance_index = structure.group(1)
                    
                    # The first two records of a file regularly contain metadata in CHAT format but on regular Toolbox tiers. Therefore, skip a record if the content of any of a few regular tiers starts with "@" (the CHAT marker for metadata tiers).
                    if ('sp' in record.keys() and re.search('^@', record['sp'])) or ('ft' in record.keys() and re.search('^@', record['ft'])):
                        continue
                
                    # Indonesian \tx and \pho regularly contain garbage taken over from CHAT -> clean BEFORE word/morpheme splits!    
                    if 'pho' in record.keys():
                        record['pho'] = re.sub('\.$|\.\.\.', '', record['pho'])
                    if 'tx' in record.keys():
                        # insecure transcriptions marked by [?]
                        if re.search('\[\?\]', record['tx']):
                            record['tx'] = re.sub('\[\?\]', '', record['tx'])
                            creadd(corpus[text_id][utterance_index], 'warnings', 'transcription insecure')
                        
                        # get sentence type from utterance delimiter. Note that the regular CHAT correspondences can't be applied to Indonesian because "!" marks imperatives and not exclamations
                        if re.search('\.', record['tx']): 
                            corpus[text_id][utterance_index]['sentence_type'] = 'default'
                        elif re.search('\?\s*$', record['tx']): 
                            corpus[text_id][utterance_index]['sentence_type'] = 'question'
                        elif re.search('\!', record['tx']): 
                            corpus[text_id][utterance_index]['sentence_type'] = 'imperative'    
                        # delete any garbage
                        record['tx'] = re.sub('[‘’\'“”\"\.!,;:\+\/]|\?$|\.\.\.|\[\?\]|<|>', '', record['tx'])
                        record['tx'] = re.sub('^0$', '', record['tx'])
                        if record['tx'] is '':
                            record.pop('tx')
                        
                # EOF Indonesian checks
                                
                # skip record if utterance_index is empty (because \ref was not well-formed)
                if not utterance_index:
                    print(file_name + ': invalid record marker "' + record['ref'] + '", skipping this record')
                    continue
                # add warning if primary transcription tier is missing or empty (\tx for Chintang, Indonesian; \text for Russian)
                if corpus_name in ['Chintang', 'Indonesian']:
                    if ('tx' not in record.keys()) or ('tx' in record.keys() and record['tx'] == ''):
                        creadd(corpus[text_id][utterance_index], 'warnings', 'empty utterance')
                elif corpus_name == 'Russian':
                    if ('text' not in record.keys()) or ('text' in record.keys() and record['text'] == ''):
                        creadd(corpus[text_id][utterance_index], 'warnings', 'empty utterance')                
                        
                # add warning if any morphology tiers are missing or empty
                for mor_tier in tbx_mor_tier_correspondences[corpus_name].keys():
                    if (mor_tier not in record.keys()) or (mor_tier in record.keys() and record[mor_tier] == ''):
                        creadd(corpus[text_id][utterance_index], 'warnings', 'not glossed')
    
                # add regular utterance-level tiers to corpus
                for tier in tbx_utt_tier_correspondences[corpus_name].keys():
                    if tier in record.keys():                        
                        tier_name_JSON = tbx_utt_tier_correspondences[corpus_name][tier]
                        creadd(corpus[text_id][utterance_index], tier_name_JSON, record[tier])
                        
                # provide 'unknown' if important values are missing    
                for tier in ['speaker_id', 'starts_at', 'ends_at']:
                    if not tier in corpus[text_id][utterance_index]: 
                        corpus[text_id][utterance_index][tier] = 'unknown'                
        
                # word-level tiers have to be split first
                for tier in tbx_word_tier_correspondences[corpus_name].keys():
                    if tier in record.keys():
                        tier_name_JSON = tbx_word_tier_correspondences[corpus_name][tier]
                        
                        # remove any trailing spaces to make split work correctly
                        record[tier] = re.sub('^\\s+|\\s+$', '', record[tier])
                        
                        # split into words and add them to corpus
                        words = re.split('\\s+', record[tier])
                        word_index = 0
                        for w in words:
                            corpus[text_id][utterance_index]['words'][word_index][tier_name_JSON] = w
                            word_index += 1
                
                # morpheme-level tiers in Toolbox have to be split in a different way from XML because there are no clear word separators
                # go through all morphemes and infer where words begin and end based on the morpheme separator "-"
                # Russian is exceptional because it does not have any segmentation - it is treated further below
                if corpus_name in ['Chintang', 'Indonesian']:
                    for tier in tbx_mor_tier_correspondences[corpus_name].keys(): 
                        tier_name_JSON = tbx_mor_tier_correspondences[corpus_name][tier]
                        if tier in record.keys():
                            morphemes = re.split('\\s+', record[tier])
                            word_index = 0
                            morpheme_index = 0
                            word_might_end_here = False
                            for m in morphemes:
                                # prefix
                                if re.search('.\-$', m):
                                    # if last morpheme was stem or suffix, start a new word
                                    if word_might_end_here == True:
                                        word_index += 1
                                        morpheme_index = 0
                                    # add morpheme to corpus dic, overwriting existing POS
                                    m = re.sub('\-', '', m)
                                    if tier_name_JSON == 'pos':
                                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = 'pfx'
                                    else:
                                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = m
                                    morpheme_index += 1
                                    # set terminator flag
                                    word_might_end_here = False
                            
                                # stem
                                elif not re.search('^\-|\-$', m):
                                    # if last morpheme was stem or suffix, start a new word
                                    if word_might_end_here == True: 
                                        word_index += 1
                                        morpheme_index = 0
                                    # add morpheme to corpus dic
                                    corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = m
                                    morpheme_index += 1
                                    # set terminator flag
                                    word_might_end_here = True
                            
                                # suffix
                                elif re.search('^\-.', m):
                                    # add morpheme to corpus dic, overwriting existing POS
                                    m = re.sub('\-', '', m)
                                    if tier_name_JSON == 'pos':
                                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = 'sfx'
                                    else:
                                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = m
                                    morpheme_index += 1
                                    # set terminator flag
                                    word_might_end_here = True
                            
                                # floating hyphen (single hyphen before word-medial prefixes and stems)
                                elif m == '-':
                                    # set terminator flag, do nothing else
                                    word_might_end_here = False
                 
                        # Russian (no segmentations!) is dealt with differently; \text is used for the word tier while \lem and \mor go to pseud-morpheme tiers (only ever 1 morpheme per word, so morpheme_index is always 0)
                elif corpus_name is 'Russian':
                    # TODO Russian has clitics, marked by the separator ~
                    
                    for tier in tbx_mor_tier_correspondences[corpus_name].keys():
                        tier_name_JSON = tbx_mor_tier_correspondences[corpus_name][tier]
                        if tier in record.keys():
                            
                            # remove any trailing spaces to make split work correctly
                            record[tier] = re.sub('^\\s+|\\s+$', '', record[tier])
                            
                            morphemes = re.split('\\s+', record[tier])
                            word_index = 0
                            for m in morphemes:
                                # ignore punctuation
                                if re.search('^([\.,;!:\"\+\-\/]+|\?)$|PUNCT|ANNOT', m):
                                    continue
                                # tier \lem contains lemmas - take every lemma as the first morpheme of the corresponding word
                                elif tier is 'lem':
                                    corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0][tier_name_JSON] = m
                                # tier \mor may contain POS and glosses - split and assign
                                elif tier is 'mor':
                                    # first check if there are both POS and glosses. "-" separates subPOS, ":" separates different glosses
                                    match_pos_or_gloss = re.search(':', m)
                                    if match_pos_or_gloss is not None:                                    
                                        # in the case of verbs and adjectives, the cutoff point between POS and glosses is the first "-", e.g. V-PST:SG:F:IRREFL:IPFV -> POS V, gloss PST.SG.F.IRREFL.IPFV
                                        match_pos_exceptions = re.search('^(V|ADJ)\-(.*)', m)
                                        if match_pos_exceptions is not None:
                                            pos = match_pos_exceptions.group(1)
                                            gloss = match_pos_exceptions.group(2)
                                        # in all other cases, the cutoff point is the first ":", e.g. PRO-DEM-NOUN:NOM:SG -> POS PRO.DEM.NOUN, gloss NOM.SG
                                        else:
                                            match_pos_and_gloss = re.search('^(.*?):(.*)', m)
                                            pos = match_pos_and_gloss.group(1)
                                            gloss = match_pos_and_gloss.group(2)
                                        pos = re.sub('\-', '.', pos)
                                        gloss = re.sub(':', '.', gloss)
                                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0][tier_name_JSON] = gloss
                                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0]['pos_target'] = pos

                                    # if there is no ":", POS and gloss are identical (e.g. for particles PCL)
                                    else:
                                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0][tier_name_JSON] = m
                                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0]['pos_target'] = m
                                word_index += 1
                            
                # check all alignments
                
                if corpus[text_id][utterance_index]['words']:
                    corpus[text_id][utterance_index]['length_in_words'] = max(corpus[text_id][utterance_index]['words'])+1
                else:
                    corpus[text_id][utterance_index]['length_in_words'] = 0
                    
                # word tiers
                if corpus[text_id][utterance_index]['length_in_words'] > 0:
                    max_index_words = corpus[text_id][utterance_index]['length_in_words']-1
                    for tier in tbx_word_tier_correspondences[corpus_name].keys():
                        if tier in record.keys():
                            tier_name_JSON = tbx_word_tier_correspondences[corpus_name][tier]
                            if not corpus[text_id][utterance_index]['words'][max_index_words][tier_name_JSON]:
                                print('alignment problem in ' + file_name + ', utterance ' + str(utterance_index) + ': all tiers should have '
                                    + str(max_index_words+1) + ' words, but ' + tier + ' (= ' + tier_name_JSON + ') has less')
                                creadd(corpus[text_id][utterance_index], 'warnings', 'broken alignment: not enough elements in ' + tier_name_JSON)
                else:
                    creadd(corpus[text_id][utterance_index], 'warnings', 'empty utterance')
                
                # morpheme tiers
                for word_index in corpus[text_id][utterance_index]['words']:
                    if corpus[text_id][utterance_index]['words'][word_index]['morphemes']:
                        max_index_morphemes = max(corpus[text_id][utterance_index]['words'][word_index]['morphemes'])
                    else:
                        max_index_morphemes = 0
                    
                    for tier in tbx_mor_tier_correspondences[corpus_name].keys():
                        tier_name_JSON = tbx_mor_tier_correspondences[corpus_name][tier]
                        if tier in record.keys():
                            # print(utterance_index, tier, len(corpus[text_id][utterance_index]['words'][word_index]['morphemes']))
                            if not corpus[text_id][utterance_index]['words'][word_index]['morphemes'][max_index_morphemes][tier_name_JSON]:
                                print('alignment problem in ' + file_name + ', utterance ' + str(utterance_index) + ', word ' + str(word_index) 
                                    + ': all words should have ' + str(max_index_morphemes+1) + ' morphemes, but ' + tier + ' (= ' + tier_name_JSON + ') has less')
                                creadd(corpus[text_id][utterance_index]['words'][word_index], 'warnings', 'broken alignment: not enough elements in ' + tier_name_JSON)
                # EOF Toolbox parser general part
                
                # corpus-specific part starts here
                if corpus_name == 'Chintang':
                    
                    # \tos and \TOS code child-directed speech ("Type Of Speech"). The addressee can be extracted from this. 
                    if 'tos' in record.keys():
                        # Only look at codes containing "directed" or "answer" - these contain addressees. For other codes (e.g. "imitation") it's not clear to whom they are directed nor whether they are always aligned with utterances at all. 
                        if re.search('directed|answer', record['tos']):
                            # reconstruct actor code for children from file name
                            match_actor_code = re.search('^(CL.*Ch)(\\d)', text_id)
                            child_prefix = match_actor_code.group(1)
                            child_number = match_actor_code.group(2)
                            # several addressees may be connected on a single tier via "+"
                            for addressee in re.split('\+', record['tos']):                                
                                addressee = re.sub('.*target\\s*child.*(\\d).*', child_prefix + '\\1', addressee)
                                addressee = re.sub('.*target\\s*child.*', child_prefix + child_number, addressee)
                                addressee = re.sub('.*child.*', 'unspecified_child', addressee)
                                addressee = re.sub('.*adult.*', 'unspecified_adult', addressee)
                                addressee = re.sub('.*non(\\s*|\\-)directed.*', 'none', addressee)
                                if not corpus[text_id][utterance_index]['addressee']:
                                    corpus[text_id][utterance_index]['addressee'] = addressee
                                else:
                                    corpus[text_id][utterance_index]['addressee'] = corpus[text_id][utterance_index]['addressee'] + ', ' + addressee
                # EOF Chintang                    
                                                
                elif corpus_name == 'Russian':
                    # \mov contains information on an associated media file (useless for us, so omit) and on starting and end point (extract)
                    if 'mov' in record.keys():
                        match_times = re.search('^\"[^\"]+\"\\s*_\\s*(\\d+)\\s*_\\s*(\\d+)\\s*$', record['mov'])
                        if match_times:
                            corpus[text_id][utterance_index]['starts_at'] = match_times.group(1)
                            corpus[text_id][utterance_index]['ends_at'] = match_times.group(2)
                    
                    # TODO punctuation, PUNCT; special characters in \text, \mor, \lem?
                
                # EOF Russian
                
                elif corpus_name == 'Indonesian':
                    # go through words once more and add corresponding target words for fragments and shortenings                    
                    for w in corpus[text_id][utterance_index]['words']:
                        if corpus[text_id][utterance_index]['words'][w]['full_word']:                            
                            # if there are brackets, actual word is word with bracket contents removed and target word is word with brackets removed, e.g. wo(rd)s: actual word = "wos", target word = "words"
                            if re.search('\(', corpus[text_id][utterance_index]['words'][w]['full_word']):
                                corpus[text_id][utterance_index]['words'][w]['full_word_target'] = re.sub('[\(\)]', '',corpus[text_id][utterance_index]['words'][w]['full_word'])
                                corpus[text_id][utterance_index]['words'][w]['full_word'] = re.sub('\([^\)]+\)', '',  corpus[text_id][utterance_index]['words'][w]['full_word'])
                            # otherwise the target word is identical to the actual word
                            else:
                                corpus[text_id][utterance_index]['words'][w]['full_word_target'] = corpus[text_id][utterance_index]['words'][w]['full_word']
                # EOF Indonesian
                            
# EOF parse_toolbox
    
# parse an open CHAT file
def parse_chat(file_name, corpus_name):

    if corpus_name == 'Inuktitut':
        pass
    
    elif corpus_name == 'Turkish_KULLD':
        pass
    
    elif corpus_name == 'Yucatec':
        pass
# EOF parse_chat