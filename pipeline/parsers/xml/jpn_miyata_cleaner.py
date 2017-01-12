# -*- coding: utf-8 -*-

import copy
import pdb
import re
import sys
import itertools

from lxml import etree
from pipeline.parsers.xml.xml_cleaner import XMLCleaner

class MiyataCleaner(XMLCleaner):

    def _process_morphology(self, u):
        pass

    def _morphology_inference(self, u):
        
        # Miyata is the only corpus with morphology coded in explicit XML style, so at least alignment doesn't have to be checked
        # note that there are two tags for compounds. <wk> (between <u> and <w>) is considered irrelevant for us and therefore removed further above in the general part. It is used rarely (21 times) and inconsistently. The other one, <mwc> (between <mor> and <mw> is part of the morphology subtree and is parsed here. 
        word_index = -1
        for w in u.findall('.//w'):
            
            morphology = w.find('mor')
            
            if morphology is not None:
                
                # prefixes can be under <mw> (default) or <mwc> (compounds), so search directly from <mor> with arbitrary depth
                for p in morphology.findall('.//mpfx'):
                    
                    m = etree.SubElement(morphology, 'm')
                    m.attrib['segments_target'] = p.text
                    m.attrib['glosses_target'] = '???'
                    m.attrib['pos_target'] = 'pfx'
                
                # stem
                m = etree.SubElement(morphology, 'm')
                # find stem by joining all stems under <w> (there may be several stems in the case of compounds)
                stems = morphology.findall('.//stem')
                stem = stems[0].text
                for i in range(1, len(stems)):
                    stem += '=' + stems[i].text
                
                # stem POS normally is under <mw>. In the case of compounds there is first one tag for the whole compound (which we take over) and then more for the individual elements (which we ignore).
                pos = morphology.findall('.//pos')
                pos = pos[0]
                main_pos = pos.find('c')
                stem_pos = main_pos.text
                for sub_pos in pos.findall('s'): 
                    stem_pos = stem_pos + '.' + sub_pos.text
                
                # stem gloss <menx>, under <mw> by default, under <mwc> for compounds
                stem_gloss = ''
                menx = morphology.find('menx')
                if menx is None:
                    stem_gloss = '???'
                else:
                    # the glosses for some clitics (=san, =kun etc.) regularly appear in <menx> instead of <mk> whereas their form is given in <mk> -> remove the gloss from <menx> and insert it at the next morpheme position (= the position of the first suffix)
                    check_clitics = re.search('((_MASC)?(_(FAM|HON|POL|'
                    'ORD|CL|NLZR|PL))(_PL)?)', menx.text)
                    if check_clitics is not None:
                        # extend morpheme list to make space for clitic
                        cl = etree.SubElement(morphology, 'm')
                        # extract clitic form
                        clitics = check_clitics.group()
                        menx.text = re.sub(clitics, '', menx.text)
                        clitics = re.sub('^_', '', clitics)
                        clitics = re.sub('_', '.', clitics)
                        cl.attrib['glosses_target'] = clitics
                        cl.attrib['type'] = 'clitic'
                    stem_gloss = menx.text
                
                m.attrib['segments_target'] = stem
                m.attrib['glosses_target'] = stem_gloss
                m.attrib['pos_target'] = stem_pos
                
                # suffixes - there are three types: sfx (default), sfxf (fused into the stem), mc (form for preceding default suffix)
                # sfx and mc can only be associated via their position in the tree, so suffixes have to be looped over using an index
                suffixes = morphology.findall('.//mk')
                
                for s in suffixes:

                    # default suffix: add to corpus, count up morphemes
                    if s.attrib['type'] == 'sfx':
                        # default: gloss is not in corpus dic yet
                        m = w.find('.//m[@type="clitic"]')
                        if m is None:
                            m = etree.SubElement(morphology, 'm')
                            m.attrib['segments_target'] = '???'
                            m.attrib['glosses_target'] = s.text
                            m.attrib['pos_target'] = 'sfx'
                        # if gloss for the suffix is already known it's been inserted from a place where it doesn't logically belong, e.g. <menx> (= the tag for stem glosses); in this case the text of <mk> gives the form, not the gloss 
                        else:
                            m.attrib['segments_target'] = s.text
                            m.attrib['pos_target'] = 'sfx'            
                            del m.attrib['type']
                        
                    # form for default suffix: add form to preceding element (= suffix), don't count up; ignore if text = "contr" (contraction)
                    elif s.attrib['type'] == 'mc' and s.text != 'contr':
                        m = w.findall('.//m')[-1]
                        m.attrib['segments_target'] = s.text
                        
                    # fused suffix: add gloss to preceding element (= stem), don't count up
                    elif s.attrib['type'] == 'sfxf':
                        # there is one particle (wa 'TOP') which is frequently fused to the copula (de+wa -> ja) and therefore treated as sfxf; the gloss is, however, not "TOP" but "wa". Add this exceptional case to the preceding stem. 
                        m = w.findall('.//m')[-1]
                        if s.text == 'wa':
                            m.attrib['segments_target'] += '.' + s.text
                        # add gloss for all other fused suffixes gloss to the gloss of the preceding stem
                        else:
                            m.attrib['glosses_target'] += '.' + s.text

                midx = -1
                for i in range(len(morphology)):
                    try:
                        midx += 1
                        if morphology[midx].tag != 'm':
                            del morphology[midx]
                            midx -= 1
                    except IndexError:
                        #print(midx, len(morphology))
                        continue

            # if there is no morphology, add warning to present word and count up
            elif morphology is None:
                XMLCleaner.creadd(w.attrib, 'warnings', 'not glossed')
    
        # EOF word loop
        
    # EOF Japanese Miyata                


if __name__ == '__main__':

    path = sys.argv[1]
    from pipeline.parsers.parsers import CorpusConfigParser as Ccp
    conf = Ccp()
    conf.read('../../ini/Japanese_Miyata.ini')
    corpus = MiyataCleaner(conf, path)

    corpus._debug_xml(sys.stdout)

