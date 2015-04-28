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

    def get_everything(self, root):
        """ method returns a list of all tag text tuples """
        everything = []
        for e in root.getiterator():
            if e is not None:
                everything.append((e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", ""), e))
        return everything

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
    #TODO: start dropping unwanted fields
    def __init__(self, path):
        Parser.__init__(self, path)
        self.metadata["participants"] = self.get_participants(self.root)
        self.metadata["session"] = self.get_session_data(self.root)
        self.metadata["project"] = self.get_project_data(self.root)
        self.metadata["media"] = self.get_media_data(self.root)
        self.write_json(self.metadata)

    def get_participants(self, root):
        participants = []
        for actor in root.Session.MDGroup.Actors.getchildren():
            participant = {}
            for e in actor.getchildren():
                t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "") # drop the IMDI stuff
                participant[t.lower()] = str(e.text) # make even booleans strings
            for k,v in participant.items():
                if k == "familysocialrole":
                    participant["speakerrole"] = participant.pop(k)
            if not len(participant) == 0:
                participants.append(participant)
        return participants

    def get_session_data(self, root):
        session = {}
        session['code'] = root.Session.Name.text
        session['date'] = root.Session.Date.text
        session['genre'] = root.Session.MDGroup.Content.Genre.text
        session['location'] = self.get_location(root)
        session['situation'] = root.Session.Description.text
        map(lambda x: x.lower(), session)
        return session

    def get_location(self, root):
        location = {}
        for e in root.Session.MDGroup.Location.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            location[t.lower()] = str(e.text)
        return location

    def get_project_data(self, root):
        project = {}
        project['name'] = root.Session.MDGroup.Project.Title.text
        project['shortname'] = root.Session.MDGroup.Project.Name.text
        project['id'] = root.Session.MDGroup.Project.Id.text
        project['contact'] = self.get_project_contact(root)
        return project

    def get_project_contact(self, root):
        contact = {}
        for e in root.Session.MDGroup.Project.Contact.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            contact[t.lower()] = str(e.text)
        return contact

    def get_media_data(self, root):
        media = {}
        for e in root.Session.Resources.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            media[t.lower()] = self.get_mediafile_data(e)
        return media

    def get_mediafile_data(self, element):
        mediafile = {}
        for e in element.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            mediafile[t.lower()] = str(e.text)
        return mediafile

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
    p = Imdi("../../corpora/Russian/metadata/IMDI/V01110710.imdi")
    # p = Chat("../../corpora/Japanese_MiiPro/xml/ArikaM/aprm19990515.xml")
    # p = Imdi("../../corpora/Chintang/metadata/yupung_Ghume.imdi")

    # for pretty print:
    # cat <input.json> | python -mjson.tool
