class XMLParser(object):

    udict = { 'source_id':None,
              'session_id_fk':None,
              'start_raw':None,
              'end_raw':None,
              'speaker_label':None,
              'addressee':None,
              'sentence_type':None,
              'translation':None,
              'comment':None,
              'warning':None          }

    mordict = { 'morphemes':None,
                'gloss_raw':None,
                'pos_raw':None    }

    def __init__(self):
        pass

    def _get_utts(self):

        for u in self.xmldoc.iter('u'):
        
            udict = {}
            words = []
            mphms = []

            for w in u.findall('.//w'):


    def _get_utts(self, debug=False):

        xmldoc = etree.parse(self.fpath).getroot()

        for elem in xmldoc.iter():
            # remove prefixed namespaces
            try:
                elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
                tag = elem.tag
                attrib = elem.attrib
            except TypeError:
                pass

        for u in xmldoc.getiterator('u'):

            try:
                #uwm = utterance - words - morphemes
                uwm = {}
                d = XMLParser.udict.copy()
                
                words = self._get_words(u)
                uwm['words'] = words

                anno = self._get_annotations(u)
                morph = anno[0]
                trans = anno[1]
                comment = anno[2]

                uwm['morphology'] = XMLParser.mordict.copy()

                for tier in morph:
                    uwm['morphology'][self.cfg['morphology_tiers'][tier]
                            ] = morph[tier]

                d['translation'] = trans
                d['comment'] = comment

                ts = self._get_timestamps(u)
                d['start_raw'] = ts[0]
                d['end_raw'] = ts[1]

                d['speaker_label'] = u.attrib.get('who')
                d['sentence_type'] = self._get_sentence_type(u)
                d['source_id'] = u.attrib.get('uID')

                d['corpus'] = self.cfg['corpus']['corpus']
                d['language'] = self.cfg['corpus']['language']

                uwm['utterance'] = d

                self._process_morphology(uwm)
                self._morphology_inference(uwm)
                self._clean_morphemes(uwm)
                uwm['utterance']['pos_raw'] = self._concat_mor_tier(
                        'pos_raw', uwm['words'])
                uwm['utterance']['gloss_raw'] = self._concat_mor_tier(
                        'gloss_raw', uwm['words'])
                uwm['utterance']['morpheme'] = self._concat_mor_tier(
                        'morpheme', uwm['words'])

                uwm['words'] = self._clean_words(uwm['words'])
                uwm['utterance']['utterance_raw'] = ' '.join(
                        [w['word'] for w in uwm['words']])


                yield uwm

            except Exception as e:
                XMLParser.logger.warn("Aborted processing of utterance {} "
                        "in file {} with error: {}\nStacktrace: {}".format(
                            u.attrib.get('uID'), self.fpath, repr(e),
                            traceback.format_exc()))

    def _clean_words(self, words):
        new_words = []
        for raw_word in words:
            word = {}
            for k in raw_word:
                if k in self.cfg['json_mappings_words']:
                    label = self.cfg['json_mappings_words'][k]
                    word[label] = raw_word[k]
                else:
                    word[k] = raw_word[k]
                    if word[k] == "":
                        word[k] = None
            word['word'] = word[self.cfg['json_mappings_words']['word']]
            new_words.append(word)
        return new_words

    def _clean_morphemes(self, mors):
        new_mword = []
        for raw_morpheme in mword:
            morpheme = {}
            for k in raw_morpheme:
                if k in self.cfg['json_mappings_morphemes']:
                    label = self.cfg['json_mappings_morphemes'][k]
                    morpheme[label] = raw_morpheme[k]
                else:
                    morpheme[k] = raw_morpheme[k]
            new_mword.append(morpheme)
        return new_mword

    def _clean_utterance(self, raw_u):

        utterance = {}
        for k in raw_u:
            if k in self.config['json_mappings_utterance']:
                label = self.config['json_mappings_utterance'][k]
                utterance[label] = raw_u[k]
            else:
                utterance[k] = raw_u[k]
        return utterance

    def _get_annotations(self, u):
        morph = {}
        trans = None
        comment = None
        for a in u.findall('.//a'):
            for tier in self.cfg['morphology_tiers']:
                if (a.attrib.get('type') == 'extension'
                        and a.attrib.get('flavor') == tier):
                    morph[tier] = a.text
            if (a.attrib.get('type') == 'english translation'):
                trans = a.text
            if (a.attrib.get('type') in ['comment', 'actions', 'explanation']):
                comment = a.text
        return morph, trans, comment

    def _get_sentence_type(self, u):
        st_raw = u.find('t').attrib.get('type')
        stype = self.cfg['correspondences'][st_raw]
        return stype

    def _get_timestamps(self, u):
        ts = u.find('.//media')
        if ts != None:
            return ts.attrib.get('start'), ts.attrib.get('end')
        else:
            return None, None

    def get_session_metadata(self):
        return self.metadata_parser.metadata['__attrs__']

    def next_speaker(self):
        for p in self.metadata_parser.metadata['participants']:
            yield p

    def next_utterance(self):
        for u in self._get_utts():
            yield u['utterance'], u['words'], u['morphemes']
