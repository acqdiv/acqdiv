from configparser import ConfigParser

from acqdiv.util.path import get_full_path
from acqdiv.util.csvparser import parse_csv


def get_roles():
    roles = ConfigParser(delimiters='=')
    roles.optionxform = str
    roles.read(get_full_path('util/resources/role_mapping.ini'))

    return roles


class RoleMapper:
    """Class for mapping various roles to and from other fields."""

    roles = get_roles()

    def __init__(self, path_label2macro_role=None):
        if path_label2macro_role:
            self.label2macro_role = parse_csv(path_label2macro_role)
        else:
            self.label2macro_role = {}

    @classmethod
    def role_raw2role(cls, role_raw):
        """Map the original role to the unified role."""
        if role_raw in cls.roles['role_mapping']:
            role = cls.roles['role_mapping'][role_raw]
            # all unknown's and none's listed in the ini become NULL
            if role != 'Unknown' and role != 'None':
                return role

        return ''

    @classmethod
    def role_raw2gender(cls, role_raw):
        """Map the original role to a gender."""
        return cls.roles['role2gender'].get(role_raw, '')
    
    @classmethod
    def role_raw2macrorole(cls, role_raw):
        """Map the original role to the macro role."""
        return cls.roles['role2macrorole'].get(role_raw, '')

    @classmethod
    def age_in_days2macrorole(cls, age_in_days):
        """Map the age to the macro role."""
        if age_in_days:
            if age_in_days <= 4380:
                return 'Child'
            else:
                return 'Adult'
        
        return ''

    def speaker_label2macrorole(self, speaker_label):
        """Map the speaker label to the macro role."""
        macrorole = self.label2macro_role.get(speaker_label, '')
        # ignore all unknown's in the ini file
        if macrorole != 'Unknown':
            return macrorole
        return ''

    def infer_macro_role(self, role_raw, age_in_days, speaker_label):
        """Infer the macro role.
        
        Inference based on: role, age and speaker label
        """
        macro_role = self.role_raw2macrorole(role_raw)
        
        if macro_role != 'Target_Child':
            macro_role = self.age_in_days2macrorole(age_in_days)

            if not macro_role:
                macro_role = self.role_raw2macrorole(role_raw)
            
            if not macro_role:
                macro_role = self.speaker_label2macrorole(speaker_label)
                
        return macro_role
