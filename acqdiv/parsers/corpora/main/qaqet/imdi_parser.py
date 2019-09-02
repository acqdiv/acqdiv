import re

from acqdiv.parsers.metadata.imdi_parser import IMDIParser


class QaqetIMDI(IMDIParser):

    def get_tc_code(self, session_code):
        return re.search(r'[A-Z]{3}', session_code).group()

    def get_participants(self):
        participants = super().get_participants()
        tc_code = self.get_tc_code(self.root.Session.Name.text)

        for participant in participants:
            if participant['code'] == tc_code:
                participant['role'] = 'Target_Child'
            else:
                participant['role'] = participant['familysocialrole']

        return participants
