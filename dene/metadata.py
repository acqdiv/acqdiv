import re, datetime, csv, logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("metadata.log", mode="w")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(object_number)d|%(funcName)s|%(levelname)s|%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def replace_i(string):
    """Replaces all instances of <ı> by <i> in a passed string and returns it"""

    letter = "ı"
    return string.replace(letter, "i")


def validate_date(date, object_number=0):
    """Checks date for sanity, input is a date as a string, if date correct, it is returned, otherwise 0"""

    try:
        year, month, day = date.split("-")
    except ValueError:
        date = re.sub(r"[./]", "-", date)

        try:
            year, month, day = date.split("-")
        except ValueError:
            logger.error("Date format wrong", extra={'object_number': object_number})
            return 0
        else:
            logger.info("Delimiter in date replaced by '-'", extra={'object_number': object_number})

    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        logger.error("Date not possible", extra={'object_number': object_number})
        return 0

    if re.fullmatch(r"\d", month):
        logger.info("Month must be two digit: added zero", extra={'object_number': object_number})
        month = "0" + month

    if re.fullmatch(r'\d', day):
        logger.info("Day must be two digit: added zero", extra={'object_number': object_number})
        day = "0" + day

    return "-".join([year, month, day])


################################################################################
################################################################################

class Session:
    """
    Class for checking the metadata of 'Session'.
    When creating a 'Session' object, you can pass the constructor a list
    containing all the metadata as a string.
    """

    session_number = 1

    def __init__(self, metadata_list=None):

        if metadata_list:
            self.code = metadata_list[0]
            self.date = metadata_list[1]
            self.situation = metadata_list[4]
            self.content = metadata_list[5]
            self.people = metadata_list[6]
            self.genre = "Discourse"
            self.subgenre = "Language acquisition"
            self.plannedness = "Spontaneous"
            self.researcher_involvement = "Non-elicited"

        else:
            self.code = ""
            self.date = ""
            self.situation = ""
            self.content = ""
            self.people = ""

        Session.session_number += 1


    def check_Code(self, participant_file):

        self.code = self.code.rstrip(" ")

        if "deslas" not in self.code:
            self.code = re.sub(r"(?i)deslas", "deslas", self.code)
            logger.info("Word 'deslas' corrected", extra={'object_number': Session.session_number})

        if re.search(r"[A-Z]{3,}", self.code):
            reader = csv.DictReader(participant_file, delimiter=",", quotechar='"')
            participant_file.seek(0)
            short_name = self.code.split("-")[1]
            for row in reader:
                if row["Short name"] == short_name:
                    break
            else:
                logger.error("Short name '" + short_name +"' does not exist in participants", extra={'object_number': Session.session_number})

            participant_file.seek(0)

        else:
            logger.error("Short name not in right format", extra={'object_number': Session.session_number})

        date_match = re.search(r"\d+[-./]\d+[-./]\d+", self.code)
        if date_match:
            possible_date = validate_date(date_match.group(), Session.session_number)

            if possible_date:
                self.code = re.sub(r"\d+[-./]\d+[-./]\d+", possible_date, self.code)
        else:
            logger.error("Date in wrong format", extra={'object_number': Session.session_number})

        if not re.fullmatch(r"deslas\-([A-Z]{3,})\-\d\d\d\d\-\d\d\-\d\d(\-[A-Z]+)?", self.code):
            logger.error("General error in code", extra={'object_number': Session.session_number})


    def check_Date(self):

        self.date = self.date.rstrip(" ")

        possible_date = validate_date(self.date, Session.session_number)

        if possible_date:
            self.date = possible_date

            if self.date[:4] < "2015":
                logger.error("Recording year is not possible", extra={'object_number': Session.session_number})

            if self.code.split("-")[2:5] != self.date.split("-"):
                logger.error("Different dates in Session.code and Session.date", extra={'object_number': Session.session_number})


    def replace_child(self):

        self.content = replace_i(self.content.rstrip(" "))
        self.situation = replace_i(self.situation.rstrip(" "))

        match = re.search(r"[A-Z]{3,}", self.code)
        if match:
            shortname = match.group()
            self.content = re.sub(r"[cC]hild(?=\W)", shortname, self.content)
            self.situation = re.sub(r"[cC]hild(?=\W)", shortname, self.situation)


    def check_Participants(self, participant_file):

        if self.people:

            self.people = replace_i(self.people.rstrip(" "))

            roles_dict = {"child": 1, "recorder":1, "mother":1, "classmate":1, "brother":1, "cousin":1, "grandmother":1, "sister":1, "father":1, "aunt":1, "uncle":1, "grandfather":1, "teacher":1, "older brother":1, "stepfather":1, "researcher":1, "older sister":1, "nephew":1, "family friend":1, "linguist":1, "great grandmother":1, "cousin":1}

            role_subs = {"auntie":"aunt", "grandma":"grandmother", "grandpa":"grandfather", "dad":"father", "mum":"mother", "step-father": "stepfather", "step-mother": "stepmother"}

            self.people = self.people.rstrip(" ")

            if re.fullmatch(r"([A-Z]{3,}\s*\(\w+([ -]\w+)*(\s*&\s*\w+)*\)[\s,]*)*[A-Z]{3,}\s*\(\w+([ -]\w+)*(\s*&\s*\w+)*\)", self.people):

                self.people = re.sub(r"([A-Z]+)(\()", r"\1 \2", self.people)
                self.people = re.sub(r"(\))([A-Z]+)", r"\1 \2", self.people)

                list_all = re.split(r"\s*,\s*|(?<=[A-Z])\s+(?=\()|(?<=\))\s+(?=[A-Z])", self.people)

                shortname_list = list_all[::2]
                role_list = list_all[1::2]

                reader = csv.DictReader(participant_file, delimiter=",", quotechar='"')
                participant_file.seek(0)

                for shortname in shortname_list:

                    for row in reader:
                        if shortname == row["Short name"]:
                            break

                    else:
                        logger.error("Shortname '" + shortname + "' does not exist in participants", extra={'object_number': Session.session_number})

                    participant_file.seek(0)

                for index1, role_set in enumerate(role_list):
                    roles = re.split('\s*&\s*', role_set[1:-1])

                    for index2, role in enumerate(roles):

                        if "of" in role:
                            match = re.search(r"(.+?)\sof\s.+$", role)

                            if match:
                                role1 = match.group(1)
                                logger.warning("'" + role + "' replaced by '" + role1 + "'", extra={'object_number': Session.session_number})
                                role = role1

                            else:
                                logger.error("'of' found in role, but not corrected", extra={'object_number': Session.session_number})

                        if role not in roles_dict:

                            if role in role_subs:
                                role = role_subs[role]
                                logger.info("Role substituted by '" + role + "'", extra={'object_number': Session.session_number})

                            else:
                                logger.warning("Role '" + role + "' not in role dictionary", extra={'object_number': Session.session_number})

                        roles[index2] = role

                    role_list[index1] = "(" + " & ".join(roles) + ")"


                self.people = ", ".join((" ".join(pair) for pair in zip(shortname_list, role_list)))


            else:
                logger.error("Format of Participants and roles not right", extra={'object_number': Session.session_number})
        else:
            logger.warning("Missing value for Participants and roles", extra={'object_number': Session.session_number})


    def check_all(self, participant_file):
        self.check_Code(participant_file)
        self.check_Date()
        self.replace_child()
        self.check_Participants(participant_file)

################################################################################
################################################################################

class Participant:
    """
    Class for checking the metadata of 'Participant'.
    When creating a 'Session' object, you can pass the constructor a list
    containing all the metadata as a string.
    """

    participant_number = 1

    def __init__(self, metadata_list=None):
        if metadata_list:
            self.shortname = metadata_list[1]
            self.birthdate = metadata_list[3]
            self.age = metadata_list[4]
            self.gender = metadata_list[5]
            self.firstlang = metadata_list[7]
            self.secondlang = metadata_list[8]
            self.mainlang = metadata_list[9]

        else:
            self.shortname = ""
            self.birthdate = ""
            self.age = ""
            self.gender = ""
            self.firstlang = ""
            self.secondlang = ""
            self.mainlang = ""

        Participant.participant_number += 1


    def check_ShortName(self, participant_file):

        self.shortname = self.shortname.rstrip(" ")

        if re.fullmatch(r"[A-Z]{3,}", self.shortname):
            counter = 0

            reader = csv.DictReader(participant_file, delimiter=",", quotechar='"')
            participant_file.seek(0)

            for row in reader:
                if row["Short name"] == self.shortname:
                    counter += 1

            participant_file.seek(0)

            if counter > 1:
                logger.warning("Shortname '" + self.shortname + "' is used twice", extra={'object_number': Participant.participant_number})

        else:
            logger.error("Short name not in right format", extra={'object_number': Participant.participant_number})


    def check_BirthDate(self):

        if self.birthdate:

            self.birthdate = self.birthdate.rstrip(" ")
            possible_date = validate_date(self.birthdate, Participant.participant_number)

            if possible_date:
                self.birthdate = possible_date
        else:
            logger.warning("Birthdate missing", extra={'object_number': Participant.participant_number})


    def check_Age(self, session_file):

        if self.age:

            self.age = self.age.rstrip(" ")

            match = re.fullmatch(r"\d+( \(\d{4}\))?", self.age)

            if match:
                if not self.birthdate and not match.group(1):
                    reader = csv.DictReader(session_file, delimiter=",", quotechar='"')
                    session_file.seek(0)

                    for row in reader:
                        if self.shortname in row["Participants and roles"]:
                            recording_date = row["Date"]
                            self.age = self.age + " (" + recording_date[:4] + ")"
                            logger.info("Recording year found and added to age", extra={'object_number': Participant.participant_number})
                            break;

                    session_file.seek(0)

            else:
                logger.error("Age not in right format", extra={'object_number': Participant.participant_number})

        else:
            logger.info("Age value missing", extra={'object_number': Participant.participant_number})


    def check_Gender(self):

        if self.gender:

            self.gender = self.gender.rstrip(" ")

            if self.gender != "Female" and self.gender != "Male":
                logger.error("Gender value not correct", extra={'object_number': Participant.participant_number})
        else:
            logger.warning("Gender value missing", extra={'object_number': Participant.participant_number})


    def check_Lang(self):

        if self.firstlang and self.secondlang and self.mainlang:
            self.firstlang = replace_i(self.firstlang.rstrip(" "))
            self.secondlang = replace_i(self.secondlang.rstrip(" "))
            self.mainlang = replace_i(self.mainlang.rstrip(" "))

            for lang in [self.firstlang, self.secondlang, self.mainlang]:
                if lang != "English" and lang != "Dene":
                    logger.warning("Language other than English and Dene", extra={'object_number': Participant.participant_number})

        else:
            logger.info("Language value missing for main language, first language or second language", extra={'object_number': Participant.participant_number})


    def check_all(self, session_file, participant_file):
        self.check_ShortName(participant_file)
        self.check_BirthDate()
        self.check_Age(session_file)
        self.check_Gender()
        self.check_Lang()


if __name__ == "__main__":

    session_file = open("sessions.csv", "r")
    participant_file1 = open("participants.csv", "r")
    # we need a second instance here, because iterating through the same File object at the same time gets very messy
    participant_file2 = open("participants.csv", "r")

    # output files containing corrected data
    new_session_file = open("sessions_new.csv", "w")
    new_participant_file = open("participants_new.csv", "w")

    fields_session = ["Code","Date","Location","Length of recording","Situation","Content","Participants and roles","Comments", "Genre", "Subgenre", "Plannedness", "Researcher involvement"]
    fields_participant = ["Added by","Short name","Full name","Birth date","Age","Gender","Education","First languages","Second languages","Main language","Language biography","Description","Contact address","E-mail/Phone"]

    reader1 = csv.reader(session_file, delimiter=",", quotechar='"')
    writer1 = csv.DictWriter(new_session_file, fieldnames=fields_session)
    # skip headers
    next(reader1, None)
    # write headers
    writer1.writeheader()

    # reading data from session metadata file
    for row in reader1:
        session = Session(row)
        session.check_all(participant_file1)

        # writing (corrected) data to new file
        writer1.writerow({"Code": session.code,
                        "Date": session.date,
                        "Location": replace_i(row[2]),
                        "Length of recording": row[3],
                        "Situation": session.situation,
                        "Content": session.content,
                        "Participants and roles": session.people,
                        "Comments": replace_i(row[7]),
                        "Genre": session.genre,
                        "Subgenre": session.subgenre,
                        "Plannedness": session.plannedness,
                        "Researcher involvement": session.researcher_involvement
                        })


    session_file.seek(0)
    participant_file1.seek(0)

    # reading data from participant metadata file
    reader2 = csv.reader(participant_file1, delimiter=",", quotechar='"')
    writer2 = csv.DictWriter(new_participant_file, fieldnames=fields_participant)
    # skip headers
    next(reader2, None)
    # write headers
    writer2.writeheader()

    for row in reader2:
        participant = Participant(row)
        participant.check_all(session_file, participant_file2)

        # writing (corrected) data to files
        writer2.writerow({"Added by": replace_i(row[0]),
                        "Short name": participant.shortname,
                        "Full name": replace_i(row[2]),
                        "Birth date": participant.birthdate,
                        "Age": participant.age,
                        "Gender": participant.gender,
                        "Education": replace_i(row[6]),
                        "First languages": participant.firstlang,
                        "Second languages": participant.secondlang,
                        "Main language": participant.mainlang,
                        "Language biography": replace_i(row[10]),
                        "Description": replace_i(row[11]),
                        "Contact address": replace_i(row[12]),
                        "E-mail/Phone": replace_i(row[13])
                        })


    session_file.close()
    participant_file1.close()
    participant_file2.close()
