
class UniqueSpeaker:
    """Data class representing a unique speaker in a corpus.

    code (str): The label of the speaker.
    name (str): The name of the speaker.
    gender_raw (str): The original gender of the speaker.
    gender (str): The cleaned gender of the speaker.
    birth_date (str): The birth date of the speaker.
    """

    code: str
    name: str
    gender_raw: str
    gender: str
    birth_date: str

    def __init__(self):
        self.code = ''
        self.name = ''
        self.gender_raw = ''
        self.gender = ''
        self.birth_date = ''
