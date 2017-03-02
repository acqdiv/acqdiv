# -*- coding: utf-8 -*-

import re
import sys
import itertools
import pdb
import xml

from lxml import etree
from .xml_cleaner import XMLCleaner

class YucatecCleaner(XMLCleaner):

    def _process_morphology(self, u):
        full_words = u.findall('.//w')
        morphology = u.find("a[@type='extension'][@flavor='mor']")
        if (morphology is not None and 
                not re.search('^\\s*[\.\?!]*\\s*$', morphology.text)):
            # remove punctuation and tags
            mortext = morphology.text
            mortext = re.sub('(^|\\s)[\.\?!\+\/]+(\\s|$)', '\\1\\2', mortext)
            mortext = re.sub('(^|\\s)tag\|\\S+(\\s|$)', '\\1\\2', mortext)
            mortext = re.sub('\\s+$', '', mortext)
            mortext = re.sub('(?<=\\s)##(?=\\s)', ' ', mortext)

            # split mor tier into words, reset counter to 0
            # Besides spaces, "&" and "+" are also interpreted as word separators (they seem to mark clitics, which tend to be treated as separate words in <w>)
            words = re.split('[\\s&\+]+', mortext)                
            new_words = []
            for w in words:

                # fixes for terrible hyphens
                w = re.sub('(:[A-Z0-9]+)\-(?=[a-záéíóúʔ]+)', '\\1|', w)
                w = re.sub('([A-Z0-9]+)\-(?=[a-záéíóúʔ]+#)', '\\1|', w)
                # If a word does not contain any of the usual morpheme separators "#" and ":" but does contain "-", this usually stands for ":"
                if not re.search('[#:|]', w) and re.search('\-', w):
                    w = re.sub('\-', ':', w)
                    w = '(usm)' + w
                # sometimes this happens on a per-morpheme level
                w = re.sub('(?<!\|)\-(?!\|)', ':', w)
                # Yucatec uses ":" both to separate glosses belonging to the same morpheme (e.g. ABS:PL) AND as a morpheme separator (stem:suffix)
                # The first case can be identified by checking for uppercase letters -> replace ":" by "."
                # TODO DEBUG
                w = re.sub('(^|[ |:])([A-Z0-9]+):(?=[A-Z0-9]+)', '\\1\\2.', w)
                # unclear words are given as "xxx" without the usual internal 
                # structure -> create structure and set 
                # both components to "unknown"
                w = re.sub('xxx', '???|???', w)
                new_words.append(w)
                            
            #initialize word index
            word_index = -1
            wlen = len(full_words)
            #mwords is a list of lists of morphemes
            for w in new_words:
                
                # count up word index, extend list if necessary
                word_index, llen = XMLCleaner.word_index_up(
                    full_words, wlen, word_index, u)

                # some words in <w> have a warning "not glossed": this means there is no element on the morphology tier corresponding to the present <w>
                # -> incremeent the <w> counter by one as long as the present morphological word is associated with the next <w>
                while(('warning' in full_words[word_index].attrib and
                    'not glossed' in full_words[word_index].attrib['warning'])
                    or 'untranscribed' in full_words[word_index].attrib):
                        word_index += 1                                                       

                
                wmor = etree.SubElement(full_words[word_index], 'mor')
                wmor.text = w

            u.remove(morphology)
                
        # if there is no morphology, add warning to complete utterance
        else:
            XMLCleaner.creadd(u.attrib, 'warning', 'not glossed')

    def _morphology_inference(self, u):

        for fw in u.findall('.//w'):

            if ('warning' in fw.attrib.keys()
                    and fw.attrib['warning'] == 'not glossed'):
                continue
            else:
                try:
                    morphemes = fw.find('.//mor')
                    w = morphemes.text
                except AttributeError:
                    XMLCleaner.creadd(fw.attrib, 'warning', 'not glossed')
                    continue

            # morphemes is a list of morphemes; initial index is -1
            morpheme_index = -1
            
            # check for prefixes first (separator "#") and split them off
            check_pfx = re.search('(^.*)#(.*$)', w)
            if check_pfx is not None:
                prefix_string = check_pfx.group(1)
                # cut out prefixes from word for further processing below
                w = check_pfx.group(2)
                for pfx in prefix_string.split('#'):
                    # count up morpheme index, extend list if necessary
                    morpheme_index += 1
                    etree.SubElement(morphemes, 'm')

                    pfx_struc = re.search('(.*)\|(.+)', pfx)
                    # structured prefixes: part before "|" is gloss, part after is phonological form
                    if pfx_struc is not None: 
                        morphemes[morpheme_index].attrib['segments_target'] = pfx_struc.group(2)
                        morphemes[morpheme_index].attrib['glosses_target'] = pfx_struc.group(1)
                        morphemes[morpheme_index].attrib['pos_target'] = 'pfx'
                    # unstructured prefixes: whole block tends to be a gloss, but not necessarily so -> throw warning
                    else:
                        morphemes[morpheme_index].attrib['segments_target'] = '???'
                        morphemes[morpheme_index].attrib['glosses_target'] = 'pfx'
                        morphemes[morpheme_index].attrib['pos_target'] = 'pfx'
                        #print(self.fpath, ' u', utterance_index, ' w', word_index, ' m', morpheme_index, ' has no segment/gloss structure: ', pfx, sep='')
                        XMLCleaner.creadd(morphemes[morpheme_index].attrib, 'warning', 'no segment/gloss structure')
            # EOF prefixes
            
            # get stem: everything up to the first ":" (= suffix separator) or, if there are no suffixes, to the end of the word
            if w.startswith('(usm)'):
                w = w[5:]
                wmors = w.split(':')
                for wmor in wmors:
                    morpheme_index += 1
                    m = etree.SubElement(morphemes, 'm')
                    m.attrib['segments_target'] = wmor
                    m.attrib['glosses_target'] = '???'
                    m.attrib['pos_target'] = '???'
                    m.attrib['warning'] = 'no segment/gloss structure'
                morphemes.text = ''
                continue


            stem = ''
            suffix_string = ''
            check_sfx = re.search('(.*?):(.*$)', w)
            if check_sfx is not None: 
                stem = check_sfx.group(1)
                suffix_string = check_sfx.group(2)
            else:
                stem = w
            # count up morpheme index, extend list if necessary
            morpheme_index += 1
            etree.SubElement(morphemes, 'm')
            stem_struc = re.search('(.*)\|(.+)', stem)
            # structured stems
            if stem_struc is not None:
                # the part after the "|" is always the phonological form of the stem
                morphemes[morpheme_index].attrib['segments_target'] = stem_struc.group(2)
                # for most stems with lexical meaning the part before the "|" is a POS
                if stem_struc.group(1) in ['3PRON', 'ADJ', 'ADV', 'AUX', 'CLFR', 'CLFR.INAN', 'CONJ', 'DEICT', 'DEM', 'DET', 'INT', 'INTERJ', 'N', 'N.PROP', 'N:PROP', 'NUM', 'PREP', 'PTL', 'QUANT', 'S', 'V', 'V.AUX', 'V:AUX', 'VI', 'V.INTRANS', 'VT', 'V.TRANS']:
                    morphemes[morpheme_index].attrib['glosses_target'] = '???'
                    morphemes[morpheme_index].attrib['pos_target'] = stem_struc.group(1)
                # for other stems it's a gloss
                else:
                    morphemes[morpheme_index].attrib['glosses_target'] = stem_struc.group(1)
                    morphemes[morpheme_index].attrib['pos_target'] = '???'   
            # unstructured stems: whole block can be a gloss or a segment -> see what it looks like and make educated guess; additionally throw warning
            else:
                # glosses_target tend to consist of uppercase letters, digits, and "."
                if re.search('^[A-Z0-9\.]+$', stem):
                    morphemes[morpheme_index].attrib['segments_target'] = '???'
                    morphemes[morpheme_index].attrib['glosses_target'] = stem
                    morphemes[morpheme_index].attrib['pos_target'] = '???'
                    #print(self.fpath, ' u', utterance_index, ' w', word_index, ' m', morpheme_index, ' has no segment/gloss structure: ', stem, sep='')
                    XMLCleaner.creadd(morphemes[morpheme_index].attrib, 'warning', 'no segment/gloss structure')
                # other stuff tends to be a segment
                else:
                    morphemes[morpheme_index].attrib['segments_target'] = stem
                    morphemes[morpheme_index].attrib['glosses_target'] = '???'
                    morphemes[morpheme_index].attrib['pos_target'] = '???'
                    #print(self.fpath, ' u', utterance_index, ' w', word_index, ' m', morpheme_index, ' has no segment/gloss structure: ', stem, sep='')
                    XMLCleaner.creadd(morphemes[morpheme_index].attrib, 'warning', 'no segment/gloss structure')
            # EOF stem
                        
            # if any suffixes were detected above, suffix_string contains them by now - otherwise it's empty
            if suffix_string:
                for sfx in suffix_string.split(':'):
                    # count up morpheme index, extend list if necessary
                    morpheme_index += 1
                    etree.SubElement(morphemes, 'm')

                    sfx_struc = re.search('(.*)\|(.+)', sfx)
                    # structured suffixes: part before "|" is gloss, part after is phonological form (+ redundant separator "-")
                    if sfx_struc is not None: 
                        morphemes[morpheme_index].attrib['segments_target'] = re.sub('^\-', '', sfx_struc.group(2))
                        morphemes[morpheme_index].attrib['glosses_target'] = sfx_struc.group(1)
                        morphemes[morpheme_index].attrib['pos_target'] = 'sfx'
                    # unstructured suffixes: whole block tends to be a gloss, but not necessarily so -> throw warning
                    else:
                        morphemes[morpheme_index].attrib['segments_target'] = '???'
                        morphemes[morpheme_index].attrib['glosses_target'] = sfx
                        morphemes[morpheme_index].attrib['pos_target'] = 'sfx'
                        #print(self.fpath, ' u', utterance_index, ' w', word_index, ' m', morpheme_index, ' has no segment/gloss structure: ', sfx, sep='')
                        XMLCleaner.creadd(morphemes[morpheme_index].attrib, 'warning', 'no segment/gloss structure')

            morphemes.text = ''

            # EOF suffixes
            
            # check if morpheme list has been filled; if not delete key
                    
            # EOF word loop


if __name__ == '__main__':
    from parsers import CorpusConfigParser as Ccp
    conf = Ccp()
    conf.read('ini/Yucatec.ini')
    corpus = YucatecCleaner(conf, 'tests/corpora/Yucatec/xml/Yucatec.xml')

    corpus._debug_xml()
