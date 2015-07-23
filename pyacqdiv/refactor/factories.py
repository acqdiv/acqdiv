import xml.etree.ElementTree as ET
from database_backend import *
from parselib import *

class Factory(object):
    def __init__(self, config):
        self.config = config

    # The following two are basically API prototypes

    def __parse(self, data):
    pass

    def __make(self):
        pass


class XmlUtteranceFactory(Factory):
    def __init__(self, config):
        super().__init__()

    def __parse(self, data):
        # this is where a lot of actual work is done
        # the question still is where we put actual corpus-specific function pointers
        # which are pretty necessary if we want to keep our modules small

        self.raw = data
        self.u = Utterance()

        self.__get_u_data()
        self.__make_words()

    def __get_u_data(self):

        # get self.rawtterance ID and speaker ID
        self.u.ID = self.raw.attrib['uID']
        self.u.SpeakerID = self.raw.attrib['who']

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
                self.u.SentenceType = t_correspondences[sentence_type.attrib['type']]
            
        # check for empty self.rawtterances, add warning
        if self.raw.find('.//w') is None:
            creadd(self.udata, 'warnings', 'empty self.rawtterance')
            # in the Japanese corpora there is a special subtype of empty self.rawtterance containing the event tag <e> 
            # (for laughing, coughing etc.) -> sentence type
            if self.raw.find('e'): 
                self.u.SentenceType = 'action'
        
        # time stamps
        time_stamp = self.raw.find('media')
        if time_stamp is not None:
            self.u.TimeStampStart = time_stamp.attrib['start']
            self.u.TimeStampEnd = time_stamp.attrib['end']

    def __make_words(self):
        # can we reduce this to one instance of self.raw.findall()?
        # that would be very helpful
        wf = self.config['word_factory']()
        for w in self.raw.findall('w'):
            if 'type' in w.attrib and w.attrib['type'] == 'omission':
                self.raw.remove(w)
        for w in self.raw.findall('.//w'):
            yield wf.make_word(w)

    def __make(self):
        pass

    def make_utterance(self, self.raw):
        self.__parse(u)
        return self.u

def XmlWordFactory(Factory):
    def __init__(self, config):
        super().__init__()

    def __parse(self, w):
        word = Word()

        # bunch of things happen here
        return word
