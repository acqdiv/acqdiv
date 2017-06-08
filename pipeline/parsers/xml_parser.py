import collections
import importlib
import io
import logging
import lxml
import re
import sys

from collections import deque
from collections import namedtuple
from lxml import etree

from pipeline.parsers.metadata import Chat
from pipeline.parsers.xml.xml_cleaner import XMLCleaner

class XMLParserFactory(object):
    """
    Callable object that dynamically loads the cleaner module for a given
    corpus and fetches the cleaner class from the names given in the .ini
    file. This allows easy extensibility: new corpora can be added simply
    by creating a new cleaner module and an .ini file for the new corpus.
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.cleaner_module = importlib.import_module(
            '.xml.' + self.cfg['paths']['cleaner'], package='parsers')
        self.cleaner_cls = eval(('self.cleaner_module.' + 
            self.cfg['paths']['cleaner_name']), globals(), locals())

    def __call__(self, fpath):
        """
        Returns a new XMLParser for the file fpath, using the current
        corpus configuration and cleaner module.
        """
        return XMLParser(self.cfg, self.cleaner_cls, fpath)

class XMLParser(object):
    """
    Parses unified XML trees into the data structures we use for the DB
    pipeline. Since every XML corpus de facto uses a different set of
    rules, and often violates its own rules, the cleaner for the appropriate
    corpus must be used to first transform the original XML into a format
    that XMLParser objects can understand.
    """

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
              'pos_raw':'???',
              'morpheme_language': '???' }

    rstruc = namedtuple('FlatUtterance', ['u', 'w', 'm']) 

    @staticmethod
    def has_value(dic, key):
        """
        Utility method to check whether key is present in the Dictionary dic
        and if yes, whether that key maps to a value other than None.
        """
        try:
            return dic[key] is not None
        except KeyError:
            return False
        except TypeError:
            return False

    @staticmethod
    def empty_except(dic, key):
        """
        Utility method to check whether key is the only
        key in Dictionary dic.
        """
        if key in dic:
            tmp = dic[key]
            del dic[key]
            ret = (dic == {})
            dic[key] = tmp
            return ret
        else:
            return dic == {}

    def __init__(self, cfg, cleaner_cls, fpath):

        self.cfg = cfg
        self.cleaner = cleaner_cls(cfg, fpath)
        self.metadata_parser = Chat(cfg, fpath)

    def _get_utts(self):
        """
        Main XMLParser method. Walks the cleaned XML tree using lxml's low-level
        iterators and extracts the appropriate Utterance, Word and Morpheme
        objects from the XML representation.

        Calls the cleaner before returning a generator object yielding
        Utterance-[Word]-[Morpheme] triples.
        """

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
                udict['translation'] = XMLCleaner.find_text(
                    u, 'translation')
                udict['comment'] = XMLCleaner.find_text(u, 'comment')

                udict['starts_at'] = XMLCleaner.find_xpath(u, 'media/@start')
                udict['ends_at'] = XMLCleaner.find_xpath(u, 'media/@end')
                udict['sentence_type'] = XMLCleaner.find_xpath(u, 't/@type')

                fws = u.findall('.//w')
                if fws is None:
                    continue
                for w in fws:

                    wdict = {}
                    #wdict['corpus'] = udict['corpus']
                    #wdict['language'] = udict['language']

                    #wdict['word_actual'] = w.find('actual').text
                    #wdict['word_target'] = w.find('target').text
                    #wdict['word'] = wdict[self.cfg['xml_mappings']['word']]

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

                    if not "dummy" in w.attrib:
                        wdict['corpus'] = udict['corpus']
                        wdict['language'] = udict['language']
                        wl = w.find('language')
                        if wl is not None:
                            wdict['word_language'] = wl.text
                        else:
                            wdict['word_language'] = udict['language']

                        wdict['word_actual'] = w.find('actual').text
                        wdict['word_target'] = w.find('target').text
                        wdict['word'] = wdict[self.cfg['xml_mappings']['word']]
                    else:
                        wdict = None

                    words.append(wdict)
                    mwords.append(morphemes)

                udict = self._clean_utterance(udict)
                words = self._clean_words(words)
                mwords = self._clean_morphemes(mwords)

                udict['pos_raw'] = self._concat_mor_tier('pos_raw', mwords)
                udict['gloss_raw'] = self._concat_mor_tier('gloss_raw', mwords)
                udict['morpheme'] = self._concat_mor_tier('morpheme', mwords)
                udict['utterance_raw'] = ' '.join([w['word'] for w in words
                                                   if XMLParser.has_value(
                                                           w, 'word')])
                udict['utterance'] = udict['utterance_raw']

                yield XMLParser.rstruc(udict, words, mwords)

            except Exception as e:
                XMLParser.logger.warning("Encountered problem processing "
                                         "utterance: {}. "
                                         "Skipping...".format(repr(e)),
                                         exc_info=sys.exc_info())

    def _clean_words(self, words):
        """
        Removes all word tiers not mentioned for extraction in the .ini files.
        """
        new_words = deque()
        for raw_word in words:
            try:
                word = {}
                for k in raw_word:
                    if k in self.cfg['xml_mappings']:
                        label = self.cfg['xml_mappings'][k]
                        word[label] = raw_word[k]
                    else:
                        word[k] = raw_word[k]
                word['word'] = word[self.cfg['xml_mappings']['word']]
            except TypeError:
                pass
            new_words.append(word)
        return new_words

    def _clean_morphemes(self, mors):
        """
        Removes all morpheme tiers not mentioned for extraction in the .ini files.
        Also ensures that all morpheme tiers taken over are the same length.
        """
        new_mors = deque()
        try:
            for mword in mors:
                new_mword = deque()
                try:
                    # extract expected morpheme tiers using the corpus config
                    for raw_morpheme in mword:
                        morpheme = {}
                        for k in raw_morpheme:
                            if k in self.cfg['xml_mappings']:
                                label = self.cfg['xml_mappings'][k]
                                morpheme[label] = raw_morpheme[k]
                            else:
                                pass
                        if not self.empty_except(morpheme, 'morpheme_language'):
                            # morpheme_language is automatically added to all morphemes,
                            # so empty morphemes are those with only that tier
                            new_mword.append(morpheme)
                    try:
                        # Flatten mword horizontally, then split into tiers.
                        # Use the flattened mword to compare the length of
                        # morpheme tiers.
                        # We use gloss_raw as the tier that determines how
                        # long the other tiers have to be.
                        # If a tier's length doesn't match up, it is set to
                        # all None.
                        flatm = {}
                        for tier in new_mword[0]:
                            flatm[tier] = [m[tier] for m in new_mword
                                           if tier in m]
                        mlen = len(flatm['gloss_raw'])
                        for tier in flatm:
                            if len(flatm[tier]) != mlen:
                                for m in new_mword:
                                    m[tier] = None
                    except IndexError:
                        continue
                    except KeyError as k:
                        XMLParser.logger.warning(
                            "Couldn't zip morpheme tiers in {}:"
                            "{}".format(self.cfg['corpus']['corpus'],
                                        repr(k)))

                    new_mors.append(new_mword)
                except TypeError:
                    continue
        except TypeError:
            pass
        return new_mors

    def _clean_utterance(self, raw_u):
        """
        Removes all utterance tiers not mentioned in the .ini files for extraction.
        """

        utterance = {}
        uvs = self.cfg['xml_mappings'].values()
        for k in raw_u:
            if k in uvs:
                if raw_u[k] in self.cfg['correspondences']:
                    utterance[k] = self.cfg['correspondences'][raw_u[k]]
                else:
                    utterance[k] = raw_u[k]
            else:
                pass
        return utterance

    def _concat_mor_tier(self, tier, morphlist):
        """
        Concatenates a morphology tier into a string for easy viewing.
        Used to create utterance level glosses.
        """
        try:
            return ' '.join(['-'.join([m for m in map(
                lambda x:
                    x[tier] if tier in x and x[tier] is not None 
                    else '???', mword)])
                for mword in morphlist])
        except TypeError:
            return None

    def get_session_metadata(self):
        """
        Method called by Processor to get session metadata.
        """
        return self.metadata_parser.metadata['__attrs__']

    def next_speaker(self):
        """
        Generator called by Processor to get speaker metadata.
        """
        for p in self.metadata_parser.metadata['participants']:
            yield p

    def next_utterance(self):
        """
        Public-facing wrapper around _get_utts().
        """
        return self._get_utts()

if __name__ == '__main__':

    from parsers import CorpusConfigParser as Ccp
    import sys

    cname = sys.argv[1]
    conf = Ccp()
    conf.read('ini/{}.ini'.format(cname))
    parser = XMLParserFactory(conf)('tests/corpora/{0}/xml/{0}.xml'.format(cname))
    i = 0
    for u in parser.next_utterance():
        i += 1
        print(u)
    print('Total utterances: {}'.format(i))
