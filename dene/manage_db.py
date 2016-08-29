import csv
import argparse
import traceback
import sys
import re
import logging

try:
    import MySQLdb as db
except ImportError:
    print("Please install mysqlclient first, e.g. by running pip3 install mysqlclient")
    sys.exit(1)

try:
    # tool for showing progress
    from tqdm import tqdm
except ImportError:
    print("Please install tqdm first, e.g. by running pip3 install tqdm")
    sys.exit(1)


class DB_Import:

    def __init__(self, con):

        self.con = con
        self.cur = self.con.cursor()
        self.args = self.commandline_setup()
        self.logger = self.get_logger()


    def commandline_setup(self):
        """Set up command line arguments"""
        arg_description = """Specify paths for metadata files"""
        parser = argparse.ArgumentParser(description=arg_description)

        parser.add_argument("--sessions", help="path to sessions.csv", default="../Metadata/sessions.csv")
        parser.add_argument("--participants", help="path to participants.csv", default="../Metadata/participants.csv")
        parser.add_argument("--files", help="path to files.csv", default="../Metadata/files.csv")
        parser.add_argument("--monitor", help="path to monitor.csv", default="../Workflow/monitor.csv")
        parser.add_argument("--locations", help="path to file_locations.csv", default="../Workflow/file_locations.csv")
        parser.add_argument("--deep", help="deletes complete database before import", action="store_true")

        return parser.parse_args()


    def get_logger(self):
        """Produce logs if database errors occur"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler("db.log", mode="w")
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(funcName)s|%(levelname)s|%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger


    def wipe(self, table, associated_tables=[]):
        """Delete all rows of a table"""
        # disable foreign key checks in all tables linked to this table
        for associated_table in associated_tables:
            self.cur.execute("""ALTER TABLE {} NOCHECK CONSTRAINT all""".format(associated_table))
            self.con.commit()

        # delete all rows
        self.cur.execute("""DELETE FROM {};""".format(table))
        self.con.commit()

        # enable foreign key checks again in all tables linked to this table
        for associated_table in associated_tables:
            self.cur.execute("""ALTER TABLE {} CHECK CONSTRAINT all""".format(associated_table))
            self.con.commit()

        # set auto-incrementing to 1
        self.cur.execute("""ALTER TABLE {} AUTO_INCREMENT = 1""".format(table))
        self.con.commit()


    def empty_str_to_none(self, row):
        "Set all empty strings to None"
        for field in row:
            if not row[field]:
                row[field] = None


    def execute(self, command, values, table, key=""):
        """Execute SQL commands and log any SQL errors."""
        if not key:
            key = str(values[0])

        try:
            self.cur.execute(command, values)
        except db.OperationalError as e:
            self.logger.error("{} : {}, {}".format(repr(e), table, key))

        except db.DataError as e:
            self.logger.error(repr(e) + ": " + key)

        self.con.commit()


    def get_insert_update_command(self, table, db_attributes, has_id=True):
        """Create INSERT with UPDATE command"""

        # check if table has a column called 'id'
        if has_id:
            return_id = ", id = LAST_INSERT_ID(id)"
        else:
            return_id = ""

        insert_update_command = """INSERT INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE {}{}""".format(
            table,
            ",".join(db_attributes),
            ",".join(["%s"]*len(db_attributes)),
            ','.join((attr + "=%s") for attr in db_attributes),
            return_id
        )

        return insert_update_command


    def import_sessions(self):
        """Refreshe table 'sessions'"""

        db_attributes = ("name", "date", "location", "duration", "situation", "content", "notes")

        command = self.get_insert_update_command("sessions", db_attributes)

        # try reading sessions.csv
        try:
            sessions_file = open(self.args.sessions, "r")
        except FileNotFoundError:
            print("Path to sessions.csv not correct!")
            sys.exit(1)

        # go through each session
        for p in tqdm(csv.DictReader(sessions_file), desc="Importing sessions"):

            self.empty_str_to_none(p)

            values = (
                p["Code"], p["Date"], p["Location"], p["Length of recording"],
                p["Situation"], p["Content"], p["Comments"]
            )

            # insert/update session
            self.execute(command, values + values, "sessions")

            # get session id in database
            self.cur.execute("""SELECT LAST_INSERT_ID()""")
            session_id = self.cur.fetchone()[0]

            # link session to participants
            self.link_sessions_participants(p["Participants and roles"], session_id, p["Code"])

        sessions_file.close()


    def link_sessions_participants(self, participants_roles, session_id, session_code=""):
        """Refresh table 'sessions_and_participants'"""

        db_attributes = ("session_fk", "participant_fk", "role")

        if participants_roles:

            # go through participants and their roles
            for part_roles in participants_roles.split(", "):

                # try to extract shortname and its roles
                try:
                    shortname, roles = re.split(r" (?=\()", part_roles)
                    # strip braces around role(s)
                    roles = roles[1:-1]
                except ValueError:
                    self.logger.error("Format of Participants and roles not correct: " + session_code)
                    continue

                # create set of roles
                role_set = set(roles.split(" & "))

                # get id of this participant with this short name
                self.cur.execute("SELECT id FROM participants WHERE short_name = '{}'".format(shortname))
                participant_id = self.cur.fetchone()

                if participant_id is None:
                    self.logger.error("Short name not in table participants: " + shortname)
                    continue

                command = self.get_insert_update_command("sessions_and_participants", db_attributes, has_id=False)

                values = (session_id, participant_id[0], role_set)

                self.execute(command, values + values, "sessions/participants", key="{}/{}".format(session_code, shortname))


    def import_participants(self):
        """Refresh table 'participants'"""

        db_attributes = (
            "short_name", "first_name", "last_name", "birthdate", "age", "gender",
            "education", "first_languages", "second_languages", "main_language",
            "language_biography", "description", "contact_address", "email_phone"
        )

        command = self.get_insert_update_command("participants", db_attributes)

        # try reading participants.csv
        try:
            participants_file = open(self.args.participants, "r")
        except FileNotFoundError:
            print("Path to participants.csv not correct!")
            sys.exit(1)

        # go through each participant
        for p in tqdm(csv.DictReader(participants_file), desc="Importing participants"):

            # convert empty strings to None
            self.empty_str_to_none(p)

            # extract first-/lastname assuming only the first can consist of more than one word
            try:
                *first_name, last_name = p["Full name"].split()
            except Exception:
                first_name = None
                last_name = None
            else:
                first_name = " ".join(first_name)

            # create sets for language fields that have more than one value
            for field in ["Main language", "First languages", "Second languages"]:
                if p[field] is not None:
                    p[field] = set(p[field].split("/"))

            # values must be in same order as its corresponding name attributes
            values = (
                p["Short name"], first_name, last_name, p["Birth date"],
                p["Age"], p["Gender"], p["Education"],
                p["First languages"], p["Second languages"], p["Main language"],
                p["Language biography"], p["Description"],
                p["Contact address"], p["E-mail/Phone"]
            )

            self.execute(command, values + values, "participants")

        participants_file.close()


    def import_monitor(self):
        """Refresh tables 'recordings' and 'progress'"""

        rec_db_attributes = (
            "name", "session_fk", "availability", "assignee_fk", "overall_quality",
            "child_speech", "directedness", "how_much_dene", "audio_quality", "notes"
        )

        progress_db_attributes = (
            "recording_fk", "task_type_fk", "task_status", "quality_check", "notes"
        )

        recordings_command = self.get_insert_update_command("recordings", rec_db_attributes)
        progress_command = self.get_insert_update_command("progress", progress_db_attributes, has_id=False)


        # try reading monitor.csv
        try:
            monitor_file = open(self.args.monitor, "r")
        except FileNotFoundError:
            print("Path to monitor.csv not correct!")
            sys.exit(1)

        # go through each recording
        for rec in tqdm(csv.DictReader(monitor_file), desc="Importing monitor"):

            # convert empty strings to None
            self.empty_str_to_none(rec)

            #******** 'recordings' stuff **********
            try:
                # try to extract session code from recording code
                session_code = re.search(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d+)?",
                    rec["recording name"]).group()
            except AttributeError:
                self.logger.error("Session code cannot be extracted from recording code: " + rec["recording name"])
                continue

            # get id of associated session
            self.cur.execute("SELECT id FROM sessions WHERE name = '{}'".format(session_code))

            try:
                session_id = self.cur.fetchone()[0]
            except TypeError:
                self.logger.error("Session code not in table sessions: " + session_code)
                continue

            # find out availability and assignee of this recording
            for task in ["segmentation", "transcription/translation", "glossing", "check transcription/translation", "check glossing"]:

                # get status of this task
                status = rec["status " + task]

                if status == "in progress":
                    availability = "assigned"
                    assignee = rec["person " + task]
                    break
                elif status == "barred":
                    availability = "barred"
                    assignee = None
                    break
                elif status == "defer":
                    availability = "defer"
                    assignee = None
                    break
            else:
                availability = "free"
                assignee = None

            # if there's assignee for a task
            if assignee:
                # get id of this assignee
                self.cur.execute("""SELECT id FROM employees
                                    WHERE CONCAT(first_name, ' ', last_name) = '{}'
                                    """.format(assignee))

                # try to get id of this assignee
                try:
                    assignee_id = self.cur.fetchone()[0]
                except TypeError:
                    self.logger.error("Assignee not in table employees: " + assignee)

            else:
                assignee_id = None

            rec_values = (
                rec["recording name"], session_id, availability, assignee_id,
                rec["quality"], rec["child speech"], rec["directedness"],
                rec["Dene"], rec["audio"], rec["notes"]
            )

            self.execute(recordings_command, rec_values + rec_values, "recordings")

            # ********** progress stuff **********

            progress_db_attributes = (
            "recording_fk", "task_type_fk", "task_status", "quality_check", "notes"
            )

            # get id of this rec in database
            self.cur.execute("""SELECT LAST_INSERT_ID()""")
            rec_id = self.cur.fetchone()[0]

            # go through each task type from monitor.csv
            for task_type in ["segmentation", "transcription/translation", "glossing"]:

                # get id of this task type
                self.cur.execute("SELECT id FROM task_types WHERE name = '{}'".format(task_type))

                try:
                    task_type_id = self.cur.fetchone()[0]
                except TypeError:
                    print("task type not found:", task_type)
                    continue

                # get status of this task
                task_status = rec["status " + task_type]

                if task_status == "barred" or task_status == "defer":
                    task_status = "not started"

                if task_type == "segmentation":
                    quality_check = "not required"
                else:
                    # get check status
                    quality_check = rec["status check " + task_type]

                progress_values = (
                    rec_id, task_type_id, task_status, quality_check, None
                )

                self.execute(progress_command, progress_values + progress_values, "progress")

        monitor_file.close()


    def import_files(self):
        """Refresh table 'files'"""

        db_attributes = (
            "name", "recording_fk", "file_type", "file_extension", "duration",
            "byte_size", "word_size", "at_UZH", "at_FNUniv", "at_CRDN", "location", "notes"
        )

        command = self.get_insert_update_command("files", db_attributes)

        # try reading sessions.csv
        try:
            files_file = open(self.args.files, "r")
        except FileNotFoundError:
            print("Path to files.csv not correct!")
            sys.exit(1)

        # try reading file_locations.csv
        try:
            locations_file = open(self.args.locations, "r")
        except FileNotFoundError:
            print("Path to file_locations.csv not correct!")
            sys.exit(1)

        # store metadata of file_locations.csv for fast retrieval
        locations = {}
        for file in csv.DictReader(locations_file):
            locations[file["File name"]] = {"at_UZH": file["UZH"],
                                            "at_FNUniv": file["FNUniv (backup F:)"],
                                            "at_CRDN": file["CRDN"],
                                            "notes": file["Notes"]}

            # TODO: what's the exact mapping?
            locations[file["File name"]] = {"at_UZH": None,
                                            "at_FNUniv": None,
                                            "at_CRDN": None,
                                            "notes": None}

        locations_file.close()


        for file in tqdm(csv.DictReader(files_file), desc="Importing files"):

            self.empty_str_to_none(file)

            # get id of recording for this file
            self.cur.execute("SELECT id FROM recordings WHERE name = '{}'".format(file["Recording code"]))

            try:
                rec_id = self.cur.fetchone()[0]
            except TypeError:
                self.logger.error("Recording code not in recordings: " + file["Recording code"])
                continue

            try:
                loc = locations[file["File name"]]
            except KeyError:
                self.logger.error("File not in file_locations.csv: " + file["File name"])
                continue

            values = (
                file["File name"], rec_id, file["Type"].lower(), file["Format"][-3:],
                file["Duration"], file["Byte size"], file["Word size"], loc["at_UZH"],
                loc["at_FNUniv"], loc["at_CRDN"], file["Location"], loc["notes"]
            )

            self.execute(command, values + values, "files")

        files_file.close()


    def import_all(self):
        """Import from all files"""
        # instead of updating all records, all records are deleted and inserted again
        if self.args.deep:
            for table in ["files", "sessions_and_participants", "progress", "recordings", "sessions", "participants"]:
                self.wipe(table)

        self.import_participants()
        print()
        self.import_sessions()
        print()
        self.import_monitor()
        print()
        self.import_files()
        print()
        print("Import finished!")


def main():

    con = db.connect(host="localhost", user="anna", passwd="anna", db="deslas", charset="utf8")

    populator = DB_Import(con)
    populator.import_all()
    con.close()


if __name__ == '__main__':
    main()
