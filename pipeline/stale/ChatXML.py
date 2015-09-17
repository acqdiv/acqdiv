""" Parse ChatXML files -- THIS IS A TEST VERSION; NOT CURRENTLY USED IN THE DB PIPELINE
"""

import sys
import contextlib
import mmap
import time
import re

# from parselib import t_correspondences as sentence_types

import xml.etree.ElementTree as ET
import collections
from lxml import objectify

NS = 'http://www.talkbank.org/ns/talkbank'

class ChatXML(object):

    """
    Data when can get:
        filename -> session_id
        text_id = root.attrib['Id'] -> transcript_id
        Date = root.attrib['Date]

    """

    def __init__(self, config, file_path):
        self.config = config
        self.path = file_path
        self.utterance = collections.OrderedDict()

        """
        # tree = ET.parse('2005-05-18.xml')
        # root = tree.getroot()
        # root.attrib
        # {'Media': '2005-05-18', 'Corpus': 'Ani', 'Mediatypes': 'audio', 'Lang': 'crl', 'Id': '2005-05-18', 'Date': '2005-05-18', 'Version': '2.0.2', '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation': 'http://www.talkbank.org/ns/talkbank http://talkbank.org/software/talkbank.xsd'}
        # k-v map in the .ini files, e.g. Id -> transcript_id
        # root.attrib['Id']
        """
        # self.etree(file_path)
        self.elxml(file_path)

    def etree(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        text_id = root.attrib['Id']
        print("TEXT_ID:", text_id)

        # gets all utterances
        for u in root.findall('.//{%s}u' % NS):
            print(u, u.tag, u.attrib)
            # corpus[text_id][utterance_index]['sentence_type'] = t_correspondences[sentence_type.attrib['type']]
            sentence_type = u.find('{%s}t' % NS)
            print(sentence_type.attrib)


        sys.exit(1)

        # gets all elements
        #for e in root.iter():
        #    print(e.tag, e.attrib)

        for elem in root.iter():
        # remove prefixed namespaces
            elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
            tag = elem.tag
            attrib = elem.attrib

        for u in root.findall('.//u'):
            print(u, u.tag, u.attrib)

        # gets all nodes
        #for node in tree.iter():
        #    print(node, node.tag, node.attrib)



        # for u in root.iter('{http://www.talkbank.org/ns/talkbank}w'):
        #    print(u.attrib)
        pass

    def elxml(self, file_path):
        tree = objectify.parse(file_path)
        root = tree.getroot()

        chat = {
            '__attrs__': self.parse_attrs(root),
            # 'participants': [self.parse_attrs(p) for p in root.Participants.participant],
            # 'comments': {c.attrib['type']: unicode(c) for c in root.comment},
            'utterances': [self.parse_utterance(u) for u in root.u]
            # 'words': [parse_word(u) for u in root.u]
        }
        #for k, v in chat.items():
        #    print(k,v)

    # TODO: map in the corpus specific attributes unless they are global in the CHATXML XSD?
    def parse_utterance(self, u):
        #print(type(u))
        res = {
            'id': u.attrib['uID'],
            'who': u.attrib['who'],
        }
        if hasattr(u, 'media'):
            res['start'] = float(u.media.attrib['start'])
            res['end'] = float(u.media.attrib['end'])

        print(u.findall('.//'))
        return res

    """
    def parse_timestamp(self, u):
        time_stamp = u.find('media')
            if time_stamp is not None:
                corpus[text_id][utterance_index]['starts_at'] = time_stamp.attrib['start']
                corpus[text_id][utterance_index]['ends_at'] = time_stamp.attrib['end']
        """
    def parse_words(self, u):
        for u in root.u:
            children = u.getchildren()
            print(children)

            #print(u.tag, u.attrib)
            #if not u.find('t'):
            #    print(u.t.attrib) # sentence type
            #print(type(u.find("media")))
            #print(u.media.attrib)
                # print(u.media.attrib)
            # print(u.findall('.//w'))
#            print(u.find('t'))

    def parse_attrs(self, e):
        return {k: e.attrib[k] for k in e.keys()}


    def get_sentence_type(self):
    # https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L198-L208
        pass


if __name__ == "__main__":
    start_time = time.time()

    from parsers import CorpusConfigParser
    cfg = CorpusConfigParser()
    cfg.read("Cree.ini")
    # f = "../../corpora/Cree/xml/Ani/2005-03-08.xml"
    f = "../../corpora/testfiles/all.xml"
    c = ChatXML(cfg, f)

    print()
    print("--- %s seconds ---" % (time.time() - start_time))
