class ChatXMLParser(SessionParser):
    """ For Cree, Inuktitut, MiiPro, Miyata, Sesotho, Turkish, & Yucatec """

    def __init__(self, config, file_path):
        SessionParser.__init__(self, config, file_path)
        self.metadata_parser = Chat(config, self.file_path)
        #TODO: can this be a self.body_parser() or something?
        with open(self.file_path, 'r') as xml:
            self.tree = ET.parse(xml)
        self.root = self.tree.getroot()
        # this creates a dictionary of child:parent pairs
        # I don't know what it's good for yet but I'm putting it in here until
        # we can figure out what rsk uses it for in his parser
        # and whether we need it.
        #self.pmap = {c:p for p in self.tree.iter() for c in p}
        self.clean_tree()

    def get_session_metadata(self):
        # Do xml-specific parsing of session metadata.
        # The config so it knows what symbols to look for.
        return self.metadata_parser.metadata['__attrs__']

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker

    def clean_tree(self):
        """ Removes prefixed namespaces """
        for elem in self.root.iter():
            elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
        #    tag = elem.tag
        #    attrib = elem.attrib
        #    #God knows what those are good for. Debugging?

    def next_utterance(self):
        # Do xml-specific parsing of utterances.
        # The config so it knows what symbols to look for.
        uf = XmlUtteranceFactory()

        for u in self.root.findall('.//u'):
            yield uf.make_utterance(u), uf.next_word, uf.next_morpheme
