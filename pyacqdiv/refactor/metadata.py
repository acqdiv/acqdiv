""" A metadata parser base class with subclasses for IMDI and CHAT XML formats
"""

import sys
import os
import re
import collections

from lxml import objectify

DEBUG = 1 # TODO: move debug to standard logging module

class Parser(object):
    """ Base metadata parser class
    """
    # do we need to pass in the config?
    # def __init__(self, config, path):
        # self.config = config

    def __init__(self, path):
        self.path = path
        self.tree = objectify.parse(path)
        self.root = self.tree.getroot()

        self.metadata = {
            '__attrs__': self.parse_attrs(self.root),
                    }
        self.metadata['__attrs__']['Cname'] = re.sub(r'\.xml.*|\.imdi.*', "", os.path.basename(str(self.path)))

        # Special case for Indonesian
        # Explanation: this converts the session ID to the same format as in the body files
        # Unless that issue was fixed in another way we will probably still want it

        # TODO: figure out what's going wrong with Indonesian
        """
        print(self.metadata['__attrs__']['Cname'])

        if self.config['corpus'] == "Indonesian":
            match = re.match(r"(\w{3})-\d{2}(\d{2})-(\d{2})-(\d{2})",self.metadata['__attrs__']['Cname'])
            self.metadata['__attrs__']['Cname'] = match.group(1).upper() + '-' + match.group(4) + match.group(3) + match.group(2)
        self.metadata['__attrs__']['schemaLocation'] = self.metadata['__attrs__'].pop('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
        """

        # assert existing_dir(self.input_path())

    def parse_attrs(self, e):
        return {k: e.attrib[k] for k in e.keys()}

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

class Imdi(Parser):
    """ subclass of metadata.Parser to deal with IMDI metadata (Chintang and Russian via S. Stoll) """

    # Do we want to load up this dictionary of everything on init
    # so that the caller has to deal with the db-specific parsing?

    # do we need to pass in the config?
    # def __init__(self, config, path):
    #    Parser.__init__(self, config, path)

    def __init__(self, path):
        Parser.__init__(self, path)
        self.metadata["participants"] = self.get_participants()
        self.metadata["session"] = self.get_session_data()
        self.metadata["project"] = self.get_project_data(self.root)
        self.metadata["media"] = self.get_media_data(self.root)

    def get_participants(self):
        """
        :return: list of participants; each participant is a dict
        of key:value, e.g. 'birthdate': '1978-03-28', 'code': 'RM'.
        Note: missing values (e.g. birthdate) skipped when not present.
        """
        participants = []
        for actor in self.root.Session.MDGroup.Actors.getchildren():
            participant = {}
            for e in actor.getchildren():
                t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "") # drop the IMDI stuff
                participant[t.lower()] = str(e.text) # make even booleans strings

            if not len(participant) == 0:
                participants.append(participant)
        return participants

    def get_session_data(self):
        session = {}
        session['id'] = self.metadata['__attrs__']['Cname']
        session['date'] = self.root.Session.Date.text
        session['genre'] = self.root.Session.MDGroup.Content.Genre.text
        session['location'] = self.get_location(self.root)
        session['situation'] = self.root.Session.Description.text
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
    # do we need to pass in the config?
    # def __init__(self, config, path):
        # Parser.__init__(self, config, path)

    def __init__(self, path):
        Parser.__init__(self, path)
        self.metadata["participants"] = self.get_participants(self.root)
        self.metadata["comments"] = self.get_comments(self.root)
        self.metadata["comments"] = self.get_comments(self.root)
        # self.write_json(self.metadata)

    # TODO: where is the get_sessions stuff? in the unifier?

    def get_participants(self, root):
        return [self.parse_attrs(p) for p in root.Participants.participant]

    def get_comments(self, root):
        #print({c.attrib['type']: str(c) for c in root.comment})
        try:
            return {c.attrib['type']: str(c) for c in root.comment}
        except:
            pass

if __name__=="__main__":
    # TODO: we need some serious tests
    # from parsers import *
    """
    print("CHINTANG:")
    imdi = Imdi("../../corpora/Chintang/metadata/CLDLCh1R01S01.imdi")
    for k, v in imdi.metadata.items():
        print(k, v)
        print()
    # print(imdi.metadata['session']['location']['address'])
    print("#########################")

    print("CREE:")
    chat = Chat("../../corpora/Cree/xml/Ani/2005-03-08.xml")
    for i in chat.metadata:
        print(i)
        print(chat.metadata[i])
        print()
    print("####")

    print("RUSSIAN:")
    imdi = Imdi("../../corpora/Russian/metadata/A00210817.imdi")
    for k, v in imdi.metadata['session'].items():
        print(k, v)
        print()
    # print(imdi.metadata['session']['location']['address'])
    print("#####################")
    """

    print("INDONESIAN:")
    # cfg = CorpusConfigParser()
    # cfg.read("Indonesian.ini")
    f = "../../corpora/Indonesian/metadata/HIZ-010601.xml"
    # chat = Chat(cfg, f)
    chat = Chat(f)
    for i in chat.metadata:
        print(i)
        print(chat.metadata[i])
        print()