from acqdiv.model.uniquespeaker import UniqueSpeaker
from typing import Optional


class Speaker:
    """Data class representing a Speaker in a Session.

    code (str): The label of the speaker.
    name (str): The name of the speaker.
    gender_raw (str): The original gender of the speaker.
    gender (str): The cleaned gender of the speaker.
    birth_date (str): The birth date of the speaker.
    age_raw (str): The original age of the speaker.
    age (str): The age of the speaker in the child language acquisition format.
    age_in_days (str): The age of the speaker in days.
    role_raw (str): The original role of the speaker.
    role (str): The unified role of the speaker.
    macro_role (str): The unified macro role of the speaker.
    languages_spoken: The languages spoken by the speaker.
    """

    uniquespeaker: Optional[UniqueSpeaker]
    code: str
    name: str
    gender_raw: str
    gender: str
    birth_date: str
    age_raw: str
    age: str
    age_in_days: str
    role_raw: str
    role: str
    macro_role: str
    languages_spoken: str

    def __init__(self):
        self.uniquespeaker = None
        self.code = ''
        self.name = ''
        self.gender_raw = ''
        self.gender = ''
        self.birth_date = ''
        self.age_raw = ''
        self.age = ''
        self.age_in_days = ''
        self.role_raw = ''
        self.role = ''
        self.macro_role = ''
        self.languages_spoken = ''
