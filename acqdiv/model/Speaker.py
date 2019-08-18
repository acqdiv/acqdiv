

class Speaker:
    """Data class representing a Speaker in a Session.

    code (str): The label of the speaker.
    name (str): The name of the speaker.
    gender_raw (str): The original gender of the speaker.
    birth_date (str): The birth date of the speaker.
    age_raw (str): The original age of the speaker.
    role_raw (str): The original role of the speaker.
    languages_spoken: The languages spoken by the speaker.
    """

    code: str
    name: str
    gender_raw: str
    birth_date: str
    age_raw: str
    role_raw: str
    languages_spoken: str

    def __init__(self):
        self.code = ''
        self.name = ''
        self.gender_raw = ''
        self.birth_date = ''
        self.age_raw = ''
        self.role_raw = ''
        self.languages_spoken = ''
