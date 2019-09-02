import re

from acqdiv.parsers.metadata.parser import MetadataParser


class IMDIParser(MetadataParser):
    """ Subclass of metadata.MetadataParser to deal with IMDI metadata (Chintang and Russian via S. Stoll) """

    def __init__(self, path):
        super().__init__(path)
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
                    for lang in actornode.xpath("*[local-name() = 'Language']"):
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
        # session['duration'] = self.get_session_duration(self.root)
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
            List: The media files and their metadata (like duration etc.).
        """
        media = {
            'mediafile': [],
            'writtenresource': [],
            'anonyms': [],
            'source': []
        }
        for e in root.Session.Resources.getchildren():
            t = e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", "")
            media[t.lower()].append(self.get_mediafile_data(e))
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


    # def get_session_duration(self, r):
    #     """
    #     get the duration of a session

    #     Args:
    #         r: root node of imdi file
    #     Returns:
    #         the session duration as an integer
    #     """
    #     try:
    #         duration = r.Session.Resources.Source.Keys.Key.text
    #         return self._format_to_seconds(duration)
    #     except AttributeError:
    #         # print("Error! No Duration extracted.")
    #         return None


    # def _format_to_seconds(self, duration):
    #     """
    #     format a string, representing session duration to seconds
    #     Args:
    #         duration: str, 'hh:mm:ss'
    #     Return:
    #         int
    #     """
    #     dur = duration
    #     h, m, s = dur.split(':')
    #     seconds = 3600*int(h)+60*int(m)+float(s)
    #     return seconds