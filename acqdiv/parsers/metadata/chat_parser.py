from acqdiv.parsers.metadata.parser import MetadataParser


class CHATParser(MetadataParser):
    """
    Subclass of metadata.MetadataParser class to deal with CHAT XML metadata extraction.

    Unlike in the IMDI files, a lot of data above session level is not
    specified in the CHATParser/Talkbank XML files, but instead saved in
    per-corpus files (with the extension .cdc). Therefor, the CHATParser class
    contains significantly less functionality than the IMDI class.
    """
    # do we need to pass in the metadata_path?
    # def __init__(self, metadata_path, path):
        # MetadataParser.__init__(self, metadata_path, path)

    def __init__(self, path):
        super().__init__(path)
        self.metadata["participants"] = self.get_participants(self.root)
        self.metadata["comments"] = self.get_comments(self.root)
        # self.metadata["session"] = self.get_session_data()

        # self.metadata["comments"] = self.get_comments(self.root)

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