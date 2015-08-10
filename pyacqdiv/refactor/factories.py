import re

import xml.etree.ElementTree as ET
from database_backend import *
from parselib import *

class Factory(object):
    def __init__(self, config=None):
        self.config = config

    # The following two are basically API prototypes

    def __parse(self, data):
        pass

    def __make(self):
        pass


class XmlUtteranceFactory(Factory):
    def __init__(self, config=None):
        super().__init__()

    def _parse(self, data):
        # this is where a lot of actual work is done
        # the question still is where we put actual corpus-specific function pointers
        # which are pretty necessary if we want to keep our modules small

        self.raw = data
        self.u = Utterance()

        self._get_u_data()
        self._clean_words()

    def _get_u_data(self):

        # get utterance ID and speaker ID
        self.u.id = self.raw.attrib['uID']
        self.u.speaker_id = self.raw.attrib['who']

        # various optional tags self.rawnder <u>
        # sentence type
        sentence_type = self.raw.find('t')
        if sentence_type is not None:
            # special Inuktitut sentence type "broken for coding": set type to default, insert warning
            if sentence_type.attrib['type'] == 'broken for coding':
                self.u.SentenceType = 'default'
                creadd(self.udata, 'warnings', 'not glossed')
            # other sentence types: get JSON equivalent from dic
            else:
                self.u.sentence_type = t_correspondences[sentence_type.attrib['type']]
            
        # check for empty utterances, add warning
        if self.raw.find('.//w') is None:
            creadd(self.udata, 'warnings', 'empty utterance')
            # in the Japanese corpora there is a special subtype of empty self.rawtterance containing the event tag <e> 
            # (for laughing, coughing etc.) -> sentence type
            if self.raw.find('e'): 
                self.u.sentence_type = 'action'
        
        # time stamps
        time_stamp = self.raw.find('media')
        if time_stamp is not None:
            self.u.timestamp_start = time_stamp.attrib['start']
            self.u.timestamp_end = time_stamp.attrib['end']

        # standard dependent tiers
        for dependent_tier in xml_dep_correspondences:
            tier = self.raw.find("a[@type='" + dependent_tier + "']")
            if tier is not None:
                try:
                    xml_dep_correspondences[dependent_tier](self.u, tier.text)
                    #TODO: put this in yucatec parser
                    #if corpus_name == 'Yucatec' and tier_name_JSON == 'english':
                    #    tier_name_db = 'spanish'
                except AttributeError:
                    print("Skipping file " + self.file_path)
                    print("Error: {0}".format(e))
                        
        # extended dependent tiers
        for extension in xml_ext_correspondences:
            tier = self.raw.find("a[@type='extension'][@flavor='" + extension + "']")
            if tier is not None: 
                xml_ext_correspondences[extension](self.u, tier.text)


    def _clean_words(self):
        # can we reduce this to one instance of self.raw.findall()?
        # that would be very helpful
        for w in self.raw.findall('w'):
            if 'type' in w.attrib and w.attrib['type'] == 'omission':
                self.raw.remove(w)

        # replacements in w.text
        for w in self.raw.findall('.//w'):
            # In ElementTree, w.text only stores the text immediately following <w>. 
            # In <w>ha<p type="drawl"/>i</w>, only 'ha' is stored as the text of <w> whereas 'i' is stored as the tail of <p>. 
            # Tags of this type are: <p> ('prosody marker'), <ca-element> ('pitch marker'), 
            # and <wk> ('word combination', marks boundaries between the elements of compounds)
            for path in ('.//p', './/ca-element', './/wk'):
                for t in w.findall(path):
                    if t.tail is not None:
                        if w.text is None:
                            w.text = t.tail
                        else:
                            w.text += t.tail
            # CHAT www, xxx, yyy all have an attribute "untranscribed" in XML; self.raw.ify text to '???'
            if 'untranscribed' in w.attrib:
                w.text = '???'
            # other replacements
            if w.text:
                # where the orthography tier is missing in Cree, <w> is not empty but contains 'missingortho' -> remove this
                w.text = re.sub('missingortho', '', w.text)
                # Sometimes words may be partially untranscribed (-xxx, xxx-, -xxx-) - transform this, too
                w.text = re.sub('\-?xxx\-?', '???', w.text)
                # only in Cree: morpheme boundaries in <w> are indicated by '_' -> remove these, segments are also given in the morphology tiers. Other corpora can have '_' in <w>, too, but there it's meaningful (e.g. for concatenating the parts of a book title treated as a single word), so only check Cree!
                # TODO: put the below in the Cree parser
                #if corpus_name == 'Cree':
                #    w.text = re.sub('_', '', w.text)
        # EOF string replacements
                                    
        # transcriptions featuring a contrast between actual and target pronunciation: go through words, create an attribute "target" (initially identical to its text), and set it as appropriate. "target" is taken self.raw. later again when all content is written to the corpus dic. 
        for w in self.raw.findall('.//w'):
            
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
        words = self.raw.findall('.//w')
        for i in range(0, len(words)):
            r = words[i].find('replacement')
            if r is not None:
                rep_words = r.findall('w')

                # go through words in replacement
                for j in range(0, len(rep_words)):
                    # check for morphology
                    mor = rep_words[j].find('mor')
                    # first word: transfer content and any morphology to parent <w> in <u>
                    if j== 0:
                        words[i].attrib['target'] = rep_words[0].attrib['target']
                        if mor is not None:
                            words[i].insert(0, mor)
                    # all further words: insert new empty <w> self.raw.der parent of last known <w> (= <u> or <g>), put content and morphology there
                    else:
                        w = ET.Element('w')
                        w.text = ''
                        w.attrib['target'] = rep_words[j].attrib['target']
                        if mor is not None:
                            w.insert(0, mor)
                        parent_map[words[i]].insert(i+j, w)
                        
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

        #g tags:
        self._resolve_groups()

    def _resolve_groups(self):
        for g in self.raw.findall('.//g'):
            words = g.findall('.//w')
            self._resolve_guesses(g, words)
            self._resolve_replacements(g, words)
            self._resolve_retracings(g, words)
            self._warn_transcriptions(g, words)

    def _resolve_guesses(self, g, words):
        # guesses at target word, e.g. <g><w>taaniu</w><ga type="alternative">nanii</ga></g>. Occasionally there may be several targets, in which case only use the first one. 
        target_guess = g.find('.//ga[@type="alternative"]')
        if target_guess is not None:
            words[0].attrib['target'] = target_guess.text

    def _resolve_replacements(self, g, words):
            # repetitions, e.g. <g><w>shoo</w><w>boo</w><r times="3"></g>: insert as many <w> groups as indicated by attrib "times" of <r>, minus 1 (-> example goes to "shoo boo shoo boo shoo boo")
            #TODO @override JPN_MiiPro
            repetitions = g.find('r')
            if repetitions is not None:
                for i in range(0, int(repetitions.attrib['times'])-1):
                    for w in words:
                        new_elem = ET.SubElement(g, 'w')
                        new_elem.text = w.text
                        # Japanese MiiPro only: repeated elements are only glossed once -> mark the word as "to be repeated" here; the morphology routine will see this and repeat the corresponding glosses. Turkish also has cases where repeated elements are only glossed once but is inconsistent; glossed repetitions seem to be more frequent overall. 
                        #if corpus_name == 'Japanese_MiiPro':
                        #    new_elem.attrib['glossed'] = 'repeated'
                        #new_elem.attrib['target'] = w.attrib['target']
                        #mor = w.find('mor')
                        #if mor is not None:
                        #    new_elem.insert(0, mor)

    def _resolve_retracings(self, g, words):
        # retracings, e.g. <g><w formType="UNIBET">shou</w><w formType="UNIBET">shou</w><k type="retracing"/></g>: search for <w> with same text and self.raw.e gloss from there; if not available set attribute 'glossed' to 'ahead'. Skip this step for Inuktitut, where retracings are regularly glossed. 
        # these are corpus-specific, so this method is defined at the XML level only for API completeness
        pass

    def _warn_transcriptions(self, g, words):
        # guessed transcriptions: add warning
        guesses = g.find('k[@type="best guess"]')
        if guesses is not None:
            for w in words:
                w.attrib['transcribed'] = 'insecure'

    def make_utterance(self, u):
        self._parse(u)
        return self.u

    def next_word(self, u):
        #words = self._clean_words()
        #wf = self.config['word_factory'](self)
        words = self.raw.findall('.//w')
        wf = XmlWordFactory(u)
        for w in words:
            yield wf.make_word(w)


class XmlWordFactory(Factory):
    def __init__(self, utterance, config=None):
        self.parent = utterance
        self.config = config

    def _parse(self, w):
        word = Word()
        word.word = w.text
        word.parent_id = self.parent.id
        return word

    def make_word(self, w):
        return self._parse(w)

    def next_morpheme(self, w):
        pass


class XmlMorphemeFactory(Factory):
    def __init__(self, word, config=None):
        self.parent = word
        self.config = config

    def _parse(self, m):
        mor = Morpheme()
        mor.morpheme = m.text
        mor.parent_id = self.parent.id
        return mor

    def make_morpheme(self, m):
        return self._parse(m)

        


        # bunch of things happen here
                        