import parsers
import factories
from parselib import *

class CreeParser(parsers.ChatXMLParser):

    def next_utterance(self):

        uf = CreeUtteranceFactory()
        
        for u in self.root.findall('.//u'):
            yield uf.make_utterance(u), uf.next_word


class CreeUtteranceFactory(factories.XmlUtteranceFactory):

    def next_word(self, u):
        #words = self._clean_words()
        #wf = self.config['word_factory'](self)
        words = self.raw.findall('.//w')
        wf = CreeWordFactory(u)
        for w in words:
            yield wf.make_word(w)

    def next_gloss(self, u):
        # Cree has four different morphology tiers that may be aligned with words <w> and require parsing
        # In order to compare the morphology tiers (e.g. for alignment), they have to be stored in a temporary Vividict before they can be added to the corpus dic
        mf = CreeMorphemeFactory(u)
        morphology = Vividict()
           
        # split morphology tiers into words
        any_morphology = False
        for morph_tier in ('tarmor', 'actmor', 'mormea', 'mortyp'):
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
                if len(words) != self.udata['length_in_words']:
                    print('alignment problem in ' + file_name + ', utterance ' + str(utterance_id) + ': general word tier <w> has ' 
                        + str(self.udata['length_in_words']) + ' words vs ' + str(len(words)) + ' in "' + morph_tier + '" (= ' 
                        + tier_name_JSON + ')')
                    creadd(self.udata, 'warnings', 'broken alignment full_word : ' + tier_name_JSON)
                                        
                # split words into morphemes, add to temporary Vividict
                word_index = 0
                for w in words:
                    morpheme_index = 0
                    morphemes = re.split('=', w)
                    for m in morphemes:
                        # some corrections where the Cree tier names don't match our target tiers exactly
                        if morph_tier == 'mortyp' and m == 'IMP' and morphology['mormea'][word_index][morpheme_index]:
                            morphology['mormea'][word_index][morpheme_index] += '.' + m
                            m = 'sfx'
                        # add morpheme to Vividict
                        morphology[morph_tier][word_index][morpheme_index] = m
                        morpheme_index += 1
                    word_index += 1                    
                
        # if there is no morphology, add warning to complete utterance
        if any_morphology == False:
            creadd(self.udata, 'warnings', 'not glossed')
        
        # after analysing all four morphology tiers, go through Vividict to check alignment and add everything to corpus dic
        # first do words
        max_length_words = max(len(morphology['mortyp']), len(morphology['mormea']), len(morphology['tarmor']), len(morphology['actmor']))
        for morph_tier in ('mortyp', 'mormea', 'tarmor', 'actmor'):
            tier_name_JSON = xml_other_correspondences[morph_tier]
            if len(morphology[morph_tier]) != max_length_words and len(morphology[morph_tier]) != 0:
                print('alignment problem in ' + file_name + ', utterance ' + str(utterance_id) + ': there should be ' 
                    + str(max_length_words) + ' words in all tiers, but ' + morph_tier + ' (=' + tier_name_JSON + ') has only ' 
                    + str(len(morphology[morph_tier]))) 
                creadd(self.udata, 'warnings', 'broken alignment between morphology tiers - word numbers don\'t match. Check' + tier_name_JSON)
            
        # go through words
        for word_index in range(-1, max_length_words):
            
            # count up word index, extend list if necessary
            word_index = list_index_up(word_index, self.udata['words'])
            
            # self.udata['words'][word_index]['morphemes'] is a list of morphemes
            self.udata['words'][word_index]['morphemes'] = []
            
            max_length_morphemes = max(len(morphology['mortyp'][word_index]), len(morphology['mormea'][word_index]), len(morphology['tarmor'][word_index]), len(morphology['actmor'][word_index]))
            for morph_tier in ('mortyp', 'mormea', 'tarmor', 'actmor'):
                tier_name_JSON = xml_other_correspondences[morph_tier]
                # check morpheme alignment
                if len(morphology[morph_tier][word_index]) != max_length_morphemes and len(morphology[morph_tier][word_index]) != 0:
                    print('alignment problem in ' + file_name + ', utterance ' + str(utterance_id) + ', word ' + str(word_index) + ': there should be ' 
                        + str(max_length_morphemes) + ' morphemes in all tiers, but ' + morph_tier + ' (=' + tier_name_JSON + ') has only ' 
                        + str(len(morphology[morph_tier][word_index])) + ' for this word')
                    creadd(self.udata['words'][word_index], 'warnings', 'broken alignment between morphology tiers - morpheme numbers don\'t match. Check ' + tier_name_JSON)    
                

                
                for m in morphology[morph_tier][word_index]:
                    if m:
                        # check for "?" attached to gloss; replace by warning that gloss is insecure
                        if re.search('\\w\?', morphology[morph_tier][word_index][morpheme_index]):
                             creadd(self.udata['words'][word_index]['morphemes'][morpheme_index], 'warnings', 'gloss insecure for tier ' + tier_name_JSON)
                             m = re.sub('\?', '', m)

                        yield mf.make_morpheme(m)

    def _resolve_groups(self):
        super()._resolve_groups()
        self._resolve_phonetic()

    def _resolve_phonetic(self):
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
                    if not self.udata[tier_name_JSON]:
                        self.udata[tier_name_JSON] = word_concatenated
                    else:
                        self.udata[tier_name_JSON] = self.udata[tier_name_JSON] + ' ' + word_concatenated

