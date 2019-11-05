from acqdiv.parsers.metadata.parser import MetadataParser


class CMDIParser(MetadataParser):

    namespace = ('{http://www.clarin.eu/cmd/1/profiles/clarin.eu:'
                 'cr1:p_1407745712035}')

    def __init__(self, path):
        super().__init__(path)
        self.metadata["participants"] = self.get_participants()
        self.metadata["session"] = self.get_session_data()
        self.metadata["media"] = self.get_media_data()

    def get_participants(self):
        participants = []
        for actor in self.root.Actors.getchildren():
            participant = {}

            for actor_node in actor.getchildren():
                actor_tag = actor_node.tag.replace(self.namespace, '')

                if actor_tag == 'Actor_Languages':
                    langlist = []
                    for lang in actor_node.iterfind(
                            self.namespace + 'Actor_Language'):
                        langlist.append(lang.Name.text)
                    if len(langlist) != 0:
                        participant['languages'] = ','.join(langlist)
                else:
                    # skip empty fields in the IMDI
                    if not str(actor_node.text).strip() == "":
                        participant[actor_tag.lower()] = \
                            str(actor_node.text).strip()

            if len(participant):
                participants.append(participant)

        return participants

    def get_session_data(self):
        session = {
            'id': self.metadata['__attrs__']['Cname'],
            'date': self.root.Date.text
        }

        return session

    def get_media_data(self):
        media = {
            'mediafile': [],
            'writtenresource': []
        }

        return media
