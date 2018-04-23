""" A metadata parser base class with subclasses for IMDI and CHAT XML formats
"""
import os
import re

from lxml import objectify

DEBUG = 1 # TODO: move debug to standard logging module

class Parser(object):
    """ Base metadata parser class.

    metadata.Parser wraps an lxml.objectify tree. It gets relevant metadata
    from the tree and exposes them in a dictionary.

    Attributes:
        metadata: A dictionary of all metadata values extracted from the
                  file the tree was initialized with.
    """
    # do we need to pass in the config?
    # def __init__(self, config, path):
        # self.config = config

    def __init__(self, config, path):
        self.path = path
        self.config = config
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
        """
        Parses and returns attributes of the root node.

        args:
            e: root node of an XML session file

        returns:
            A dictionary of all attributes of e.
        """
        return {k: e.attrib[k] for k in e.keys()}


    def get_everything(self, root):
        """
        Parses and returns a list of all tag tuples in the tree.

        args:
            root: Root node of an XML session file

        returns:
            a list of tuples, each representing all tags of a node
        """
        everything = []
        for e in root.getiterator():
            if e is not None:
                everything.append((e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", ""), e))
        return everything


class Imdi(Parser):
    """ Subclass of metadata.Parser to deal with IMDI metadata (Chintang and Russian via S. Stoll) """

    # Do we want to load up this dictionary of everything on init
    # so that the caller has to deal with the db-specific parsing?

    # do we need to pass in the config?
    # def __init__(self, config, path):
    #    Parser.__init__(self, config, path)

    def __init__(self, config, path):
        Parser.__init__(self, config, path)
        self.metadata["participants"] = self.get_participants()
        self.metadata["session"] = self.get_session_data()
        self.metadata["project"] = self.get_project_data(self.root)
        self.metadata["media"] = self.get_media_data(self.root)


    def get_participants(self):
        """
        Get a list of session participants.

        Parses the session tree, collecting information about
        all participants in a dictionary.

        Returns:
            A list of dictionaries representing participants. The
            participant's child nodes are keys with their text as values.
            Note: missing values (e.g. birthdate) skipped when not present.
        """
        participants = []
        for actor in self.root.Session.MDGroup.Actors.getchildren():
            participant = {}

            # go through actor nodes, paying special attention to complex nodes
            for actornode in actor.getchildren():
                actortag = actornode.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "") # drop the IMDI stuff

                # deal with special nodes first
                # <Languages>: this may contain several languages -> save as list
                if actortag == 'Languages':
                    langlist = []
                    for lang in actornode.iterfind('Language'):
                        if lang.Id.text != None:
                            try:
                                langlist.append(lang.Id.text.split(':')[1])
                            except IndexError:
                                langlist.append(lang.Id.text)
                    if len(langlist) != 0:
                        participant[actortag.lower()] = " ".join(langlist)
                # <Keys>: marks family relations which may be used for role inference when given in relation to the current target child
                elif actortag == 'Keys':
                    # get code for current target child from session name
                    search_tc_session = re.search('^CL(.+?Ch\\d)R\\d+S\\d+$', str(self.root.Session.Name.text))
                    if search_tc_session is not None:
                        current_target_child = search_tc_session.group(1)
                        # find Key where Name = "FSR_" + the code of the current target child
                        for key in actornode.iterfind('Key'):
                            if re.search('FSR_'+current_target_child, key.get('Name')):
                                participant['family_key'] = str(key.text)

                # all other nodes: simply add to dictionary
                else:
                    if not str(actornode.text).strip() == "": # skip empty fields in the IMDI
                        participant[actortag.lower()] = str(actornode.text).strip() # turn booleans into strings

            # check collected participant dictionary, then append to list of all participants
            if not len(participant) == 0:
                # Chintang only: special role inference
                # Default for participant['role'] is the value taken from the field Role; overwrite this by more specific value UNLESS the existing value is "Target Child"

                if self.config['corpus']['corpus'] == "Chintang":
                    # (1) Actor/FamilySocialRole is on average more specific than Actor/Role
                    if ('familysocialrole' in participant and
                        participant['familysocialrole'] not in ['Unspecified', 'unspecified'] and
                        participant['role'] not in ['target child', 'Target child', 'Target Child']):
                        participant['role'] = participant['familysocialrole']
                    # (2) Even better values can sometimes be found in Actor/Keys. This list of nodes has been evaluated above; the relevant value is now in participant['family_key']
                    if ('family_key' in participant and
                        participant['family_key'] not in ['None', 'none', 'n/a', '?', '??'] and
                        participant['role'] not in ['target child', 'Target child', 'Target Child']):
                        participant['role'] = participant['family_key']

                participants.append(participant)
        return participants


    def get_session_data(self):
        """
        Get session-level metadata.

        Returns:
            A dictionary of session metadata nodes.
        """
        session = {}
        session['id'] = self.metadata['__attrs__']['Cname']
        session['date'] = self.root.Session.Date.text
        session['genre'] = self.root.Session.MDGroup.Content.Genre.text
        session['location'] = self.get_location(self.root)
        session['situation'] = self.root.Session.Description.text
        map(lambda x: x.lower(), session)
        return session


    def get_location(self, root):
        """
        Get metadata about recording location.

        Args:
            root: Root node of the session XML.

        Returns:
            A dictionary containing location metadata.
        """
        location = {}
        for e in root.Session.MDGroup.Location.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            location[t.lower()] = str(e.text)
        return location


    def get_project_data(self, root):
        """
        Get project-level metadata.

        Args:
            root: Root node of the session XML.

        Returns:
            A dictionary containing location metadata.
        """
        project = {}
        project['name'] = root.Session.MDGroup.Project.Title.text
        project['shortname'] = root.Session.MDGroup.Project.Name.text
        project['id'] = root.Session.MDGroup.Project.Id.text
        project['contact'] = self.get_project_contact(root)
        return project


    def get_project_contact(self, root):
        """
        Get contact data of the project owner.

        Args:
            root: Root node of the session XML.

        Returns:
            A dictionary containing contact data for the project owner.
        """
        contact = {}
        for e in root.Session.MDGroup.Project.Contact.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            contact[t.lower()] = str(e.text)
        return contact


    def get_media_data(self, root):
        """
        Get data about session multimedia resources.

        If there are audio or video files and positions specified,
        return these data. Otherwise returns an empty dictionary.

        Args:
            root: Root node of the session XML.

        Returns:
            A dictionary of media files and metadata (like duration etc.)
        """
        media = {}
        for e in root.Session.Resources.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            media[t.lower()] = self.get_mediafile_data(e)
        return media


    def get_mediafile_data(self, element):
        """
        Helper method to get metadata for individual multimedia resources.

        Args:
            element: A child node of a media node.

        Returns:
            A dictionary of mediafile data.
        """
        mediafile = {}
        for e in element.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            mediafile[t.lower()] = str(e.text)
        return mediafile


class Chat(Parser):
    """
    Subclass of metadata.Parser class to deal with CHAT XML metadata extraction.

    Unlike in the IMDI files, a lot of data above session level is not
    specified in the Chat/Talkbank XML files, but instead saved in
    per-corpus files (with the extension .cdc). Therefor, the Chat class
    contains significantly less functionality than the IMDI class.
    """
    # do we need to pass in the config?
    # def __init__(self, config, path):
        # Parser.__init__(self, config, path)

    def __init__(self, config, path):
        Parser.__init__(self, config, path)
        self.metadata["participants"] = self.get_participants(self.root)
        self.metadata["comments"] = self.get_comments(self.root)
        # self.metadata["session"] = self.get_session_data()

        # self.metadata["comments"] = self.get_comments(self.root)
        # self.write_json(self.metadata)

    # TODO: where is the get_sessions stuff? in the unifier?


    def get_participants(self, root):
        """
        Get a list of all session participants.

        Iterate through the participants node, building a list of dictionaries.
        In Talkbank XML, data about participants is encoded as attributes of a
        participant node, rather than child nodes as in IMDI. Each participant
        is a dictionary of the form {attr key: attr value, ...}.

        Args:
            root: Root node of the session XML.

        Returns:
            A list of dictionaries containing participant metadata.
        """
        return [self.parse_attrs(p) for p in root.Participants.participant]


    def get_comments(self, root):
        """
        Extract miscellaneous metadata from Talkbank XML.

        In the non-IMDI corpora, all non-participant metadata are stored in
        child nodes of the comment node. This method performs a simple
        dictionary comprehension to extract them.

        Args:
            root: Root node of the session XML.

        Returns:
            A dictionary with metadata. If an error occurs, do nothing.
        """
        #print({c.attrib['type']: str(c) for c in root.comment})
        try:
            return {c.attrib['type']: str(c) for c in root.comment}
        except Exception:
            pass


if __name__=="__main__":
    # TODO: we need some serious tests
    from acqdiv.parsers.parsers import CorpusConfigParser as ccp

    print("INDONESIAN:")
    # cfg = CorpusConfigParser()
    cfg = ccp()
    cfg.read("Indonesian.ini")
    f = "../corpora/Indonesian/xml/HIZ-1999-06-05.xml"
    chat = Chat(cfg, f)
    # chat = Chat(f)
    for i in chat.metadata:
        print(i)
        print(chat.metadata[i])
        print()
    print("#########################")

    print("CHINTANG:")
    cfg = ccp()
    cfg.read("Chintang.ini")
    imdi = Imdi(cfg, "../corpora/Chintang/imdi/CLDLCh1R01S01.imdi")
    for k, v in imdi.metadata.items():
        print(k, v)
        print()
    # print(imdi.metadata['session']['location']['address'])
    print("#########################")

    print("RUSSIAN: ")
    cfg = ccp()
    cfg.read("Russian.ini")
    imdi = Imdi(cfg, "../corpora/Russian/imdi/A00410909.imdi")
    for k, v in imdi.metadata.items():
        print(k, v)
        print()
    # print(imdi.metadata['session']['location']['address'])
    print("#########################")

    print("JPN_MIYATA:")
    cfg = ccp()
    cfg.read("JapaneseMiyata.ini")
    chat = Chat(cfg, "../corpora/Cree/xml/aki10610.xml")
    for i in chat.metadata:
        print(i)
        print(chat.metadata[i])
        print()
    print("#########################")
