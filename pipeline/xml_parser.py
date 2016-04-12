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
