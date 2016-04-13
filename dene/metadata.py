"""Checks and corrects the metadata for sessions and participants.

This modules implements two classes for checking and correcting the metadata of sessions and participants.
It also includes two module-level functions, one for replacing all <ı>'s and one checking the date for sanity.

If the module is run directly, it reads the files 'sessions.csv' and 'participants.csv' and checks all their fields,
then writes the (corrected) data to the files 'sessions_new.csv' and 'participants_new.csv'.

Example:
    python3 metadata.py

Author:
    Anna Jancso (anna.jancso@uzh.ch)
"""

import re
import datetime
import csv
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("metadata.log", mode="w")
handler.setLevel(logging.INFO)

# object_number: this is the line where a session or participant occurs in their respective files
# object_id: this is what identifies a session (Session.Code) or participant (Participant.Short name).
formatter = logging.Formatter("%(object_number)d|%(object_id)s|%(funcName)s|%(levelname)s|%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def replace_i(string):
    """Replace all instances of <ı> by <i>.

    Positional args:
        string: any string

    Returns:
        (corrected) string
    """
    letter = "ı"
    return string.replace(letter, "i")


def validate_date(str_date, object_number=0, object_id=""):
    """Check date for sanity and correct it.

    Positional Args:
        str_date: date as a string

    Keyword Args:
        object_number: the number of the class instance for logging
        object_id: this identifies the class instance for logging

    Returns:
        empty string if date is not correct, otherwise the (corrected) date
    """
    # try to parse any of the three given date formats
    for format_index, format in enumerate(["%Y-%m-%d", "%Y.%m.%d", "%Y/%m/%d"]):
        try:
            date = datetime.datetime.strptime(str_date, format)
        except:
            pass
        else:
            # check if date delimiter was '-'
            if format_index != 0:
                logger.info("Delimiter in Session.date replaced by '-'",
                    extra={"object_number": object_number, "object_id": object_id})

            return date.strftime("%Y-%m-%d")

    # if date cannot be parsed with any of the given formats, produce warning and return empty string
    logger.error("Date cannot be parsed - date is not possible or the required format \d{4}-\d{2}-\d{2} is wrong",
        extra={"object_number": object_number, "object_id": object_id})
    return ""


################################################################################
################################################################################

class Session:
    """Class for checking and correcting the metadata of a session."""

    # keep track of the line where the session occurs in the session table
    session_number = 1

    def __init__(self, shortname_list, code="", date="", situation="", content="", people=""):
        """Store all field values of a session that must be checked in instance variables.

        Positional args:
            shortname_list: list storing all shortnames (Participant.Short name) from the participants table

        Keyword args:
            all fields that must be checked can be optionally passed as a string, default value is an empty string
        """
        self.code = code
        self.date = date
        self.situation = situation
        self.content = content
        self.people = people
        self.genre = "Discourse"
        self.subgenre = "Language acquisition"
        self.plannedness = "Spontaneous"
        self.researcher_involvement = "Non-elicited"
        self.shortname_list = shortname_list

        # increment every time a new Session instance is created
        Session.session_number += 1


    def check_Code(self):
        """Check and correct the code (Session.Code).

        Note:
            The prescribed format is <desla-shortname-year-month-day[-partial_session_letter]>.
        """
        self.code = self.code.rstrip(" ")

        if "deslas" not in self.code:
            # desla must be lowercased, so try to correct it by lowercasing it
            self.code = re.sub(r"(?i)deslas", "deslas", self.code)
            logger.info("'deslas' lowercased", extra={"object_number": Session.session_number, "object_id": self.code})

        # check the shortname, it must be at least 3 chars long and uppercased
        # to avoid the matching of the uppercased 'DESLA', we specify in the regex
        # that 'desla' must precede and a number must follow the date
        match = re.search(r"deslas\-([A-Z]{3,})\-\d+", self.code)
        if match:
            short_name = match.group(1)
            # Check if the shortname occurs in the list of shortnames
            if short_name not in self.shortname_list:

                logger.error("Short name '" + short_name +"' does not exist in participants",
                    extra={"object_number": Session.session_number, "object_id": self.code})

        else:
            logger.error("Shortname cannot be parsed - expected format is [A-Z]{3,}",
                extra={"object_number": Session.session_number, "object_id": self.code})

        # regex for extracting date part
        date_match = re.search(r"\d+[-./]\d+[-./]\d+", self.code)
        if date_match:
            # check, correct and replace date
            self.code = re.sub(r"\d+[-./]\d+[-./]\d+",
                validate_date(date_match.group(), Session.session_number, self.code), self.code)
        else:
            logger.error("Date in wrong format", extra={"object_number": Session.session_number, "object_id": self.code})

        # after all corrections being made before, finally check if the format of the code is now right
        if not re.fullmatch(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-[A-Z]+)?", self.code):
            logger.error("General error in code", extra={"object_number": Session.session_number, "object_id": self.code})


    def check_Date(self):
        """Check if the recording date (Session.Date) is 2015 or later and if it matches the one in Session.code."""
        self.date = self.date.rstrip(" ")
        self.date = validate_date(self.date, Session.session_number, self.code)

        if self.date:

            # Check if recording year is 2015 or later
            if self.date[:4] < "2015":
                logger.error("Recording year is not possible",
                    extra={"object_number": Session.session_number, "object_id": self.code})

            # Extract the date in Session.code and compare it to the date in Session.date
            if self.code.split("-")[2:5] != self.date.split("-"):
                logger.error("Different dates in Session.code and Session.date",
                    extra={"object_number": Session.session_number, "object_id": self.code})


    def replace_child(self):
        """Replace all instances of 'child' in Session.content and Session.situation by the shortname."""
        self.content = replace_i(self.content.rstrip(" "))
        self.situation = replace_i(self.situation.rstrip(" "))

        match = re.search(r"deslas\-([A-Z]{3,})\-\d+", self.code)
        if match:
            shortname = match.group()
            self.content = re.sub(r"[cC]hild(?=\W)", shortname, self.content)
            self.situation = re.sub(r"[cC]hild(?=\W)", shortname, self.situation)


    def check_Participants(self):
        """Check and correct the participants and roles (Session.Participants and roles).

        Note:
            The prescribed format is <shortname (role [& role]), shortname (role [& role]), ...>.
        """
        if self.people:

            # a set of predefined roles which can be extended if needed
            role_table = {
                "child", "recorder", "mother", "classmate", "brother",
                "cousin", "grandmother", "sister", "father", "aunt",
                "uncle", "grandfather", "teacher", "older brother", "stepfather",
                "researcher", "older sister", "nephew", "family friend", "linguist",
                "great grandmother", "cousin"
            }

            # hash for replacing certain informal terms or non-standard spellings
            role_subs = {
                "auntie": "aunt", "grandma": "grandmother", "grandpa": "grandfather",
                "dad": "father", "mum": "mother", "step-father": "stepfather",
                "step-mother": "stepmother"
            }

            # sometimes commas occur at the end of the participant and roles, so strip them away too
            self.people = replace_i(self.people.rstrip(" ").rstrip(","))

            part_role_regex = re.compile(r"""
                (
                [A-Z]{3,}               # Shortname must be at least 3 chars long
                \s*                     # an optional whitespace
                \(                      # an opening bracket
                \w+([ -]\w+)*           # a role which can consist of multiple words, sometimes separated by a hyphen
                (\s*[&,]\s*             # if there are multiple roles for a shortname, they are separated by an ampersand or comma
                \w+([ -]\w+)*           # same as second last line
                )*                      # can repeat pattern: role1 & role2 & role3 ...
                \)                      # a closing bracket
                [\s,]*                  # shortname-role pairs can be separated by a comma or by an optional whitespace
                )+                      # can repeat pattern: shortname (role set), shortname (role set), ...
                """, re.VERBOSE)

            if part_role_regex.fullmatch(self.people):

                # insert a whitespace between shortname and role (in brackets)
                self.people = re.sub(r"([A-Z]+)(\()", r"\1 \2", self.people)
                # insert a whitespace between role (in brackets) and shortname
                self.people = re.sub(r"(\))([A-Z]+)", r"\1 \2", self.people)

                # create list containing all shortnames and roles by splitting at whitespaces between shortname and role and
                # at whitespaces and commas between role and shortname
                list_all = re.split(r"(?<=[A-Z])\s+(?=\()|(?<=\))\s*[, ]\s*(?=[A-Z])", self.people)

                # extract all shortnames by taking out every even element
                shortname_list = list_all[::2]
                # extract all roles by taking out every odd element
                role_list = list_all[1::2]

                # check if all shortnames also occur in the shortname list (i.e. in Participant.Short name)
                for shortname in shortname_list:

                    if shortname not in self.shortname_list:
                        logger.error("Shortname '" + shortname + "' does not exist in participants",
                            extra={"object_number": Session.session_number, "object_id": self.code})

                # go through the roles of every shortname
                for role_set_index, role_set in enumerate(role_list):

                    # store role(s) of a shortname in a list by stripping away the braces and splitting at ampersand
                    roles = re.split('\s*[&,]\s*', role_set[1:-1])

                    # now go through all roles of that shortname
                    for role_index, role in enumerate(roles):

                        # check if there is an 'of' in any of the roles
                        if "of" in role:
                            # the pattern should be <role of role>
                            match = re.search(r"(.+?)\sof\s.+$", role)

                            if match:
                                # extract only the first role
                                role1 = match.group(1)

                                logger.warning("'" + role + "' replaced by '" + role1 + "'",
                                    extra={"object_number": Session.session_number, "object_id": self.code})

                                # and save it without the second role
                                role = role1

                            else:
                                logger.error("'of' found in role, but not corrected",
                                    extra={"object_number": Session.session_number, "object_id": self.code})

                        # check if the role occurs in the predefined set of roles
                        if role not in role_table:

                            # check if the role must be replaced by a more formal term
                            if role in role_subs:
                                logger.info("Role '" + role + "' substituted by '" + role_subs[role] + "'",
                                    extra={"object_number": Session.session_number, "object_id": self.code})

                                # replace it and save it
                                role = role_subs[role]

                            else:
                                logger.warning("Role '" + role + "' not in role dictionary",
                                    extra={"object_number": Session.session_number, "object_id": self.code})

                        # finally save the (corrected) role in the right place in the roles list of a shortname
                        roles[role_index] = role

                    # merge all (corrected) roles of a shortname
                    role_list[role_set_index] = "(" + " & ".join(roles) + ")"

                # merge all shortnames and their corresponding roles
                self.people = ", ".join((" ".join(pair) for pair in zip(shortname_list, role_list)))


            else:
                logger.error("Participants and roles cannot be parsed",
                    extra={"object_number": Session.session_number, "object_id": self.code})
        else:
            logger.warning("Missing value for Participants and roles",
                extra={"object_number": Session.session_number, "object_id": self.code})


    def check_all(self):
        """Check all fields of a session."""
        self.check_Code()
        self.check_Date()
        self.replace_child()
        self.check_Participants()

################################################################################
################################################################################

class Participant:
    """Class for checking and correcting the metadata of a participant."""

    # keep track of the line where the participant occurs in the file
    participant_number = 1

    def __init__(self, shortname_list, date_partrole_list , shortname="", birthdate="",
                age="", gender="", firstlang="", mainlang=""):
        """Store all field values of a participant that must be checked in instance variables.

        Positional args:
            shortname_list:     list storing all shortnames (Participant.Short name) from the participants table
            date_partrole_list: list storing dates (Session.date) and participants and their roles (Session.Participant and roles)
                                from the sessions table

        Keyword args:
            all fields that must be checked can be optionally passed as a string, default value is an empty string
        """
        self.shortname = shortname
        self.birthdate = birthdate
        self.age = age
        self.gender = gender
        self.firstlang = firstlang
        self.mainlang = mainlang
        self.shortname_list = shortname_list
        self.date_partrole_list = date_partrole_list

        # increment every time a new Participant instance is created
        Participant.participant_number += 1


    def check_ShortName(self):
        """Check if shortname is in the correct format and if it does not occur more than once in the participants table."""
        self.shortname = self.shortname.rstrip(" ")

        # shortname must be at least 3 chars long and uppercased
        if re.fullmatch(r"[A-Z]{3,}", self.shortname):
            counter = 0

            # count how often the shortname occurs in the list of shortnames
            for shortname in self.shortname_list:
                if self.shortname == shortname:
                    counter += 1

            # if it occurs more than once, produce warning
            if counter > 1:
                logger.warning("Shortname '" + self.shortname + "' is used twice",
                    extra={"object_number": Participant.participant_number, "object_id": self.shortname})

        else:
            logger.error("Shortname cannot be parsed - expected format is [A-Z]{3,}",
                extra={"object_number": Participant.participant_number, "object_id": self.shortname})


    def check_BirthDate(self):
        """Check birth of date (Participant.Birth date) for sanity."""
        if self.birthdate:
            self.birthdate = self.birthdate.rstrip(" ")
            self.birthdate = validate_date(self.birthdate, Participant.participant_number, self.shortname)

        else:
            logger.warning("Birthdate missing",
                extra={"object_number": Participant.participant_number, "object_id": self.shortname})


    def check_Age(self):
        """Check if the age field (Participant.Age) is in the correct format.

        If the date of birth (Participant.Birth date) is missing but the age is known but there is no year,
        try to find the first recording where the participant appears in the list of participants and roles and
        get the year from there.

        Note:
            The prescribed format is <number[ (year)]>.
        """
        if self.age:

            self.age = self.age.rstrip(" ")

            # age value must be a number optionally followed by a year in brackets
            match = re.fullmatch(r"\d+( \(\d{4}\))?", self.age)

            if match:

                # check if date of birth and year is missing
                if not self.birthdate and not match.group(1):

                    # go through the list of dates and participants and roles
                    for date, partrole in date_partrole_list:

                        # if the shortname is among the participants and roles of a session
                        if self.shortname in partrole:
                            # save the corresponding date of the session
                            recording_date = date
                            # add it to the age value by extracting the year only
                            self.age = self.age + " (" + recording_date[:4] + ")"
                            logger.info("Date of birth is missing, but age is known - recording year is added",
                                extra={"object_number": Participant.participant_number, "object_id": self.shortname})

                            break

            else:
                logger.error("Age cannot be parsed - expected format is \d+( \(\d{4}\))?",
                    extra={"object_number": Participant.participant_number, "object_id": self.shortname})

        else:
            logger.info("Age value missing", extra={"object_number": Participant.participant_number, "object_id": self.shortname})


    def check_Gender(self):
        """Check if the gender field has either the value Female or Male."""
        if self.gender:
            self.gender = self.gender.rstrip(" ")

            if self.gender != "Female" and self.gender != "Male":
                logger.error("Gender value not correct",
                    extra={"object_number": Participant.participant_number, "object_id": self.shortname})
        else:
            logger.warning("Gender value missing",
                extra={"object_number": Participant.participant_number, "object_id": self.shortname})


    def check_Lang(self):
        """Check if the language fields have the values English or Dene."""
        if self.firstlang and self.mainlang:
            self.firstlang = replace_i(self.firstlang.rstrip(" "))
            self.mainlang = replace_i(self.mainlang.rstrip(" "))

            for lang in [self.firstlang, self.mainlang]:
                if lang != "English" and lang != "Dene":
                    logger.warning("Language other than English and Dene",
                        extra={"object_number": Participant.participant_number, "object_id": self.shortname})

        else:
            logger.info("Language value missing for main language or first language",
                extra={"object_number": Participant.participant_number, "object_id": self.shortname})


    def check_all(self):
        """Check all fields of a participant."""
        self.check_ShortName()
        self.check_BirthDate()
        self.check_Age()
        self.check_Gender()
        self.check_Lang()


if __name__ == "__main__":

    # open session (sessions.csv) and participant (participants.csv) file for reading
    session_file = open("sessions.csv", "r")
    participant_file = open("participants.csv", "r")

    # open output files where the corrected data will be written to
    new_session_file = open("sessions_new.csv", "w")
    new_participant_file = open("participants_new.csv", "w")

    # create DictReader and DictWriter instance for the sessions
    sessions_reader = csv.DictReader(session_file, delimiter=",", quotechar='"')
    sessions_writer = csv.DictWriter(new_session_file, fieldnames=sessions_reader.fieldnames)

    # create DictReader and DictWriter instance for the participants
    participants_reader = csv.DictReader(participant_file, delimiter=",", quotechar='"')
    participants_writer = csv.DictWriter(new_participant_file, fieldnames=participants_reader.fieldnames)

    # create list that stores all shortnames occuring in the participants table
    shortname_list = [row["Short name"] for row in participants_reader]

    # create list that stores the dates and the participants and roles occuring in the sessions table as a tuple
    date_partrole_list = [(row["Date"], row["Participants and roles"]) for row in sessions_reader]

    # reset file pointers since we already iterated the files when creating the two lists above
    session_file.seek(0)
    participant_file.seek(0)

    # the file pointers are now on the first line, so go to next line to skip the headers
    next(sessions_reader)
    next(participants_reader)

    # write headers
    sessions_writer.writeheader()
    participants_writer.writeheader()

    # read the metadata of each session line by line from the file 'sessions.csv'
    for row in sessions_reader:

        # create an instance of the Session class with the metadata of the session
        session = Session(shortname_list,
                        code=row["Code"],
                        date=row["Date"],
                        situation=row["Situation"],
                        content=row["Content"],
                        people=row["Participants and roles"])

        # check all fields of the session
        session.check_all()

        # write (corrected) data of the session to the output file 'sessions_new.csv'
        sessions_writer.writerow({"Code": session.code,
                        "Date": session.date,
                        "Location": replace_i(row["Location"].rstrip(" ")),
                        "Length of recording": row["Length of recording"].rstrip(" "),
                        "Situation": session.situation,
                        "Content": session.content,
                        "Participants and roles": session.people,
                        "Comments": replace_i(row["Comments"].rstrip(" "))
                        # "Genre": session.genre,
                        # "Subgenre": session.subgenre,
                        # "Plannedness": session.plannedness,
                        # "Researcher involvement": session.researcher_involvement
                        })

    # read the metadata of each participant line by line from the file 'participants.csv'
    for row in participants_reader:

        # create an instance of the Participant class with the metadata of the participant
        participant = Participant(shortname_list, date_partrole_list,
                                shortname=row["Short name"],
                                birthdate=row["Birth date"],
                                age=row["Age"],
                                gender=row["Gender"],
                                firstlang=row["First languages"],
                                mainlang=row["Main language"])

        # check all fields of the participant
        participant.check_all()

        # write (corrected) data of the session to the output file 'participants_new.csv'
        participants_writer.writerow({"Added by": replace_i(row["Added by"].rstrip(" ")),
                        "Short name": participant.shortname,
                        "Full name": replace_i(row["Full name"].rstrip(" ")),
                        "Birth date": participant.birthdate,
                        "Age": participant.age,
                        "Gender": participant.gender,
                        "Education": replace_i(row["Education"].rstrip(" ")),
                        "First languages": participant.firstlang,
                        "Second languages": replace_i(row["Second languages"].rstrip(" ")),
                        "Main language": participant.mainlang,
                        "Language biography": replace_i(row["Language biography"].rstrip(" ")),
                        "Description": replace_i(row["Description"].rstrip(" ")),
                        "Contact address": replace_i(row["Contact address"].rstrip(" ")),
                        "E-mail/Phone": replace_i(row["E-mail/Phone"].rstrip(" "))
                        })


    session_file.close()
    participant_file.close()
    new_session_file.close()
    new_participant_file.close()
    handler.close()
