from acqdiv.parsers.metadata.imdi_parser import IMDIParser
import re


class ChintangIMDIParser(IMDIParser):

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
                # Chintang only: special role inference
                # Default for participant['role'] is the value taken from the field Role; overwrite this by more specific value UNLESS the existing value is "Target Child"

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
