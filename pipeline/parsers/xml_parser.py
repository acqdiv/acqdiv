import collections
import importlib
import io
import logging
import lxml
import pdb
import re
import sys

from collections import deque
from collections import namedtuple
from lxml import etree

from .metadata import Chat
from .xml.xml_cleaner import XMLCleaner

class XMLParserFactory(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.cleaner_module = importlib.import_module(
            '.xml.' + self.cfg['paths']['cleaner'], package='parsers')
        self.cleaner_cls = eval(('self.cleaner_module.' + 
            self.cfg['paths']['cleaner_name']), globals(), locals())

    def __call__(self, fpath):
        return XMLParser(self.cfg, self.cleaner_cls, fpath)

class XMLParser(object):

    logger = logging.getLogger('pipeline.' + __name__)

    udict = { 'utterance_id':None,
              'session_id_fk':None,
              'starts_at':None,
              'ends_at':None,
              'speaker_label':None,
              'addressee':None,
              'sentence_type':None,
              'translation':None,
              'comment':None,
              'warning':None          }

    mdict = { 'morphemes':'???',
              'gloss_raw':'???',
              'pos_raw':'???'    }

    rstruc = namedtuple('FlatUtterance', ['u', 'w', 'm']) 

    def __init__(self, cfg, cleaner_cls, fpath):

        self.cfg = cfg
        self.cleaner = cleaner_cls(cfg, fpath)
        self.metadata_parser = Chat(cfg, fpath)

    def _get_utts(self):

        xmldoc = self.cleaner.clean()

        #for elem in xmldoc.iter():
        #    # remove prefixed namespaces
        #    try:
        #        elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
        #        tag = elem.tag
        #        attrib = elem.attrib
        #    except TypeError:
        #        pass

        for u in xmldoc.getiterator('u'):

            udict = XMLParser.udict.copy()
            words = deque()
            mwords = deque()

            try:

                udict['corpus'] = self.cfg['corpus']['corpus']
                udict['language'] = self.cfg['corpus']['language']

                udict['utterance_id'] = u.attrib.get('uID')
                udict['speaker_label'] = u.attrib.get('who')
                udict['warning'] = u.attrib.get('warning')

                udict['addressee'] = XMLCleaner.find_text(u, 'addressee')
                udict['translation'] = XMLCleaner.find_text(u, 'translation')
                udict['comment'] = XMLCleaner.find_text(u, 'comment')

                udict['starts_at'] = XMLCleaner.find_xpath(u, 'media/@start')
                udict['ends_at'] = XMLCleaner.find_xpath(u, 'media/@end')
                udict['sentence_type'] = XMLCleaner.find_xpath(u, 't/@type')

                fws = u.findall('.//w')
                if fws is None:
                    continue
                for w in fws:

                    wdict = {}

                    wdict['corpus'] = udict['corpus']
                    wdict['language'] = udict['language']

                    wdict['word_actual'] = w.find('actual').text
                    wdict['word_target'] = w.find('target').text
                    wdict['word'] = wdict[self.cfg['xml_mappings']['word']]
                    wdict['warning'] = w.attrib.get('warning')

                    if ((udict['warning'] is not None
                        and 'not glossed' in udict['warning']) 
                        or (wdict['warning'] is not None
                            and 'not glossed' in wdict['warning'])):
                        morphemes = None
                    else:
                        morphemes = deque()
                        for m in w.findall('.//m'):
                            mdict = {}
                            for tier_name in m.attrib:
                                mdict[tier_name] = m.attrib.get(tier_name)
                            morphemes.append(mdict)

                    words.append(wdict)
                    mwords.append(morphemes)

                udict = self._clean_utterance(udict)
                words = self._clean_words(words)
                mwords = self._clean_morphemes(mwords)

                udict['pos_raw'] = self._concat_mor_tier('pos_raw', mwords)
                udict['gloss_raw'] = self._concat_mor_tier('gloss_raw', mwords)
                udict['morpheme'] = self._concat_mor_tier('morpheme', mwords)
                udict['utterance_raw'] = ' '.join([w['word'] for w in words
                                                   if w['word'] is not None])
                udict['utterance'] = udict['utterance_raw']

                yield XMLParser.rstruc(udict, words, mwords)

            except Exception as e:
                XMLParser.logger.warning("Encountered problem processing "
                                         "utterance: {}. "
                                         "Skipping...".format(repr(e)),
                                         exc_info=sys.exc_info())

    def _clean_words(self, words):
        new_words = deque()
        try:
            for raw_word in words:
                word = {}
                for k in raw_word:
                    if k in self.cfg['xml_mappings']:
                        label = self.cfg['xml_mappings'][k]
                        word[label] = raw_word[k]
                    else:
                        pass
                word['word'] = word[self.cfg['xml_mappings']['word']]
                new_words.append(word)
        except TypeError:
            pass
        return new_words

    def _clean_morphemes(self, mors):
        new_mors = deque()
        try:
            for mword in mors:
                new_mword = deque()
                try:
                    for raw_morpheme in mword:
                        morpheme = {}
                        for k in raw_morpheme:
                            if k in self.cfg['xml_mappings']:
                                label = self.cfg['xml_mappings'][k]
                                morpheme[label] = raw_morpheme[k]
                            else:
                                pass
                        if morpheme != {}:
                            new_mword.append(morpheme)
                    new_mors.append(new_mword)
                except TypeError:
                    continue
        except TypeError:
            pass
        return new_mors

    def _clean_utterance(self, raw_u):

        utterance = {}
        for k in raw_u:
            if k in self.cfg['xml_mappings']:
                label = self.cfg['xml_mappings'][k]
                if raw_u[k] in self.cfg['correspondences']:
                    utterance[label] = self.cfg['correspondences'][raw_u[k]]
                else:
                    utterance[label] = raw_u[k]
            else:
                pass
        return utterance

    def _concat_mor_tier(self, tier, morphlist):
        try:
            return ' '.join(['-'.join([m for m in map(
                lambda x:
                    x[tier] if tier in x and x[tier] is not None 
                    else '???', mword)])
                for mword in morphlist])
        except TypeError:
            return None

    def get_session_metadata(self):
        return self.metadata_parser.metadata['__attrs__']

    def next_speaker(self):
        for p in self.metadata_parser.metadata['participants']:
            yield p

    def next_utterance(self):
        return self._get_utts()

if __name__ == '__main__':

    from inuktitut_cleaner import InuktitutCleaner
    from parsers import CorpusConfigParser as Ccp
    import sys
    
    cname = sys.argv[1]
    conf = Ccp()
    conf.read('ini/{}.ini'.format(cname))
    corpus = InuktitutCleaner
    parser = XMLParser(conf, corpus, 'tests/corpora/{0}/xml/{0}.xml'.format(cname))
    i = 0
    for u in parser.next_utterance():
        i += 1
        print(u)
    print('Total utterances: {}'.format(i))
