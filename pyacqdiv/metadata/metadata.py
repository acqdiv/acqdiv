"""
A parser base class

Metadata formats:

- IMDI (Russian; Chintang)
- CHAT XML (the converted CHAT corpora)

TODO (@bambooforest): 
- how and where to dump the json wrt cli.py
- add lxml objectify to setup.py

"""

import sys
import json
from lxml import objectify
# import pyacqdiv # here we need to tie in with the cli
# from metadata import util # here we will get the age calculator

DEBUG = 1

class Parser(object):
    """
    Expected directory layout for extracting metadata

    metadata/
      - <corpus.id>
        - original-filename.xml.json == json output files
        - <corpus.id>_metadata.csv (csv table of all metadata; to add)
        """

    def __init__(self, path):
        self.tree = objectify.parse(path)
        self.root = self.tree.getroot()

        self.metadata = {
            '__attrs__': self.parse_attrs(self.root),
        }
        # assert existing_dir(self.input_path())

    def parse_attrs(self, e):
        return {k: e.attrib[k] for k in e.keys()}

    def input_path(self, *comps):
        # TODO
        return os.path.join(os.path.join(self.cleaning_path(), '.input'), *comps)

    def cleaning_path(self, *comps):
        return os.path.join(
            existing_dir(os.path.join(self.cfg['cleaning_dir'], self.id)), *comps)


    # where to write the json files

    def validate(self, src, schema):
        """ validate a set of xml files """
        # can be done from the command line given xmllint and an xsd:
        # xmllint --noout --schema IMDI_3.0.xsd 
        pass

    def corpora_metadata(self, src):
        """ extract corpus level (.cdc) metadata from chat corpora """
        # see acqdiv/extraction/metadata/corpora.py
        pass

    def sessions_metadata(self, src):
        """ extract sesssion level metadata from chat xml corpora using NLTK """
        # see acqdiv/extraction/metadata/sessions.py
        pass

    def get_participants(self):
        """ get participants; metadata type specific methods in the subclasses """
        pass

    def write_json(self, output): 
        # with open(path + '.json', 'w') as fp:
        with open('temp.json', 'w') as fp:
            if DEBUG:
                try:
                    json.dump(output, fp)
                except:
                    print("Skipped object " + repr(output) + " of type " + str(type(output)))
            else:
                json.dump(output, fp)


class Imdi(Parser):
    """ subclass of metadata.Parser to deal with IMDI metadata (Chintang and Russian via S. Stoll) """
    def __init__(self, path):
        Parser.__init__(self, path)
        self.metadata["participants"] = self.get_participants(self.root)
        self.write_json(self.metadata)

    def get_participants(self, root):
        participants = {}
        for e in root.Session.MDGroup.Actors.Actor.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            for tag in e:
                if not tag == "":
                    participants[t.lower()] = str(tag) # make even booleans strings

        # TODO: convert to standard chat / acqdiv header categories 
        # below is an example: "familysocialrole" -> "role")
        for k, v in participants.items():
            if v == "familysocialrole":
                participants["role"] = participants.pop(k)
        return participants
        

class Chat(Parser):
    """ subclass of metadata.Parser class to deal with CHAT XML metadata extraction """
    def __init__(self, path):
        Parser.__init__(self, path)
        self.metadata["participants"] = self.get_participants(self.root)
        self.metadata["comments"] = self.get_comments(self.root)
        self.write_json(self.metadata)

    def get_participants(self, root):
        return [self.parse_attrs(p) for p in root.Participants.participant]

    def get_comments(self, root):
        #print({c.attrib['type']: str(c) for c in root.comment})
        return {c.attrib['type']: str(c) for c in root.comment}

if __name__=="__main__":
    # p = Parser("../../corpora/Russian/metadata/IMDI/V01110710.imdi")
    # p = Imdi("../../corpora/Russian/metadata/IMDI/V01110710.imdi")
    # p = Chat("../../corpora/Japanese_MiiPro/xml/ArikaM/aprm19990515.xml")
    p = Imdi("../../corpora/Chintang/metadata/yupung_Ghume.imdi")

    # for pretty print:
    # cat <input.json> | python -mjson.tool
