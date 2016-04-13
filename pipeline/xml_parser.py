import collections
import importlib
import io
import logging
import lxml
import metadata
import pdb
import re
import traceback
import xml_cleaner

from collections import deque
from collections import namedtuple
from lxml import etree
from metadata import Chat
from xml_cleaner import XMLCleaner

class XMLParserFactory(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.CorpusCleaner = importlib.import_module(self.cfg['paths']['cleaner'])
        self.cleaner_cls = eval(('self.CorpusCleaner.' + 
            self.cfg['paths']['cleaner_name']), globals(), locals())

    def __call__(self, fpath):
        return XMLParser(self.cfg, self.cleaner_cls, fpath)

class XMLParser(object):

    logging.basicConfig(filemode='w')
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('errors.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

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

    mdict = { 'morphemes':None,
              'gloss_raw':None,
              'pos_raw':None    }

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

                udict['source_id'] = u.attrib.get('uID')
                udict['speaker_label'] = u.attrib.get('who')
                udict['warning'] = u.attrib.get('warning')

                udict['addressee'] = XMLCleaner.find_text(u, 'addressee')
                udict['translation'] = XMLCleaner.find_text(u, 'translation')
                udict['comment'] = XMLCleaner.find_text(u, 'comment')

                udict['start_raw'] = XMLCleaner.find_xpath(u, 'media/@start')
                udict['end_raw'] = XMLCleaner.find_xpath(u, 'media/@end')
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
                    wdict['word'] = wdict[self.cfg['json_mappings']['word']]
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
                            for tier_name in self.cfg['json_mappings_morphemes']:
                                new_tier = self.cfg['json_mappings_morphemes'][tier_name]
                                mdict[new_tier] = m.attrib.get(tier_name)
                            morphemes.append(mdict)

                    words.append(wdict)
                    mwords.append(morphemes)

                yield XMLParser.rstruc(udict, words, mwords)

            except Exception as e:
                XMLParser.logger.warn("Encountered problem processing "
                                      "utterance: {}\n{}"
                                      "Skipping...".format(repr(e), 
                                          traceback.format_exc()))

    def _clean_words(self, words):
        new_words = []
        for raw_word in words:
            word = {}
            for k in raw_word:
                if k in self.cfg['json_mappings']:
                    label = self.cfg['json_mappings'][k]
                    word[label] = raw_word[k]
                else:
                    word[k] = raw_word[k]
                    if word[k] == "":
                        word[k] = None
            word['word'] = word[self.cfg['json_mappings']['word']]
            new_words.append(word)
        return new_words

    def _clean_morphemes(self, mors):
        new_mors = []
        for mword in mors:
            new_mword = []
            for raw_morpheme in mword:
                morpheme = {}
                for k in raw_morpheme:
                    if k in self.cfg['json_mappings']:
                        label = self.cfg['json_mappings'][k]
                        morpheme[label] = raw_morpheme[k]
                    else:
                        morpheme[k] = raw_morpheme[k]
                new_mword.append(morpheme)
            new_mors.append(new_mword)
        return new_mors

    def _clean_utterance(self, raw_u):

        utterance = {}
        for k in raw_u:
            if k in self.config['json_mappings']:
                label = self.config['json_mappings'][k]
                utterance[label] = raw_u[k]
            else:
                utterance[k] = raw_u[k]
        return utterance

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
    
    conf = Ccp()
    conf.read('ini/Inuktitut.ini')
    corpus = InuktitutCleaner(conf, 'tests/corpora/Inuktitut/xml/Inuktitut.xml')
    xmlb = corpus.clean()
    parser = XMLParser(conf, xmlb)
    for u in parser.next_utterance():
        print(u)
