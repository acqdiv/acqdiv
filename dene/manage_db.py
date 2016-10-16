"""Module providing classes for interacting with the Dene database.

This module can be used to manipulate the database over the terminal by using
one of the following commands: import, export, send, assign, update, reassign,
checkin, letcheck, feedback, handover, reset, create.
For more details on these commands, run python3 db_manager.py [command] --help.

The following external python modules (which can be installed by pip) are used:
    - mysqlclient (interface to MySQL)
    - tqdm (progress meter)
"""

import os
import re
import sys
import csv
import logging
import warnings
import argparse

try:
    import MySQLdb as db
    import MySQLdb.cursors
except ImportError:
    print("Please install mysqlclient first!")
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    print("Please install tqdm first!")
    sys.exit(1)


class DB_Manager:
    """Interface for working with the Dene database"""

    def __init__(self, host, user, passwd, database, charset="utf8"):
        """Establish a database connection.

        Positional args:
            Specify host, user, password and a database name
        Optional args:
            Specify a character set to be used
        """
        self.con = db.connect(host=host, user=user, passwd=passwd,
                              db=database, charset=charset)

    def __enter__(self):
        """Return class object."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close database connection."""
        self.con.close()

    def start(self):
        """Start main application.

        Command line arguments are parsed to determine action to be taken.
        """
        # get command line parser
        parser = self.get_parser()
        # parse all of its arguments and store them
        self.args = parser.parse_args()

        # get cursor (for 'export' the special one 'DictCursor')
        if self.args.command != "export":
            self.cur = self.con.cursor()
        else:
            self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)

        # execute appropriate action function
        self.args.func()

    def get_parser(self):
        """Get command line parser."""
        # TODO: it might be sensible to make this more modular
        # if this method gets larger and more complex

        # get main parser
        parser = argparse.ArgumentParser()
        # add subparsers that will hold the subcommands
        subparsers = parser.add_subparsers()

        # add subcommand 'import'
        import_parser = subparsers.add_parser(
            "import", help="Import metadata from csv files to database")
        import_parser.set_defaults(command="import", func=self.imp)

        for name1, name2, hlp, default in [
                ("-s", "--sessions", "path to sessions.csv",
                 "../Metadata/sessions.csv"),
                ("-p", "--participants", "path to participants.csv",
                 "../Metadata/participants.csv"),
                ("-f", "--files", "path to files.csv",
                 "../Metadata/files.csv"),
                ("-m", "--monitor", "path to monitor.csv",
                 "../Workflow/monitor.csv"),
                ("-l", "--locations", "path to file_locations.csv",
                 "../Workflow/file_locations.csv")
                ]:

            import_parser.add_argument(name1, name2, help=hlp, default=default)

        import_parser.add_argument(
            "-r", "--radical", help="deletes complete database before import",
            action="store_true")

        # add subcommand checkin
        checkin_parser = subparsers.add_parser(
            "checkin", help="Upload file and set corresponding task status"
                            + " to 'complete'or 'incomplete'")
        checkin_parser.set_defaults(command="checkin", func=self.checkin)

        checkin_parser.add_argument("file", help="file name")
        checkin_parser.add_argument("status", help="set task status",
                                    choices=["complete", "incomplete"])
        checkin_parser.add_argument("--checked", help="task is checked",
                                    action="store_true")
        checkin_parser.add_argument("--notes", help="notes")

        # add all other subcommands
        for command, cmd_hlp, func, args in [
                ("export",
                 "Export metadata from database to csv files",
                 self.exp,
                 [("--path", "directory path where files are saved")]),
                ("send",
                 "Send latest version of a file to a person.",
                 self.send,
                 [("file", "file name"),
                  ("recipient", "recipient"),
                  ("--notes", "notes")]),
                ("assign",
                 "Assign recording to a person for a task.",
                 self.assign,
                 [("rec", "recording name"),
                  ("assignee", "assignee"), ("task", "task"),
                  ("--notes", "notes")]),
                ("update",
                 "Upload new version of file"
                 + "without changing workflow status.",
                 self.update,
                 [("file", "file name"),
                  ("--notes", "notes")]),
                ("reassign",
                 "Assign running task to a different person.",
                 self.reassign,
                 [("rec", "recording name"),
                  ("assignee", "assignee"),
                  ("--notes", "notes")]),
                ("letcheck",
                 "Assign recording to specialist for feedback.",
                 self.letcheck,
                 [("rec", "recording name"),
                  ("assignee", "assignee"),
                  ("--notes", "notes")]),
                ("next",
                 "Have same assignee do the next task"
                 + "in the predefined order.",
                 self.next,
                 [("rec", "recording name"),
                  ("--notes", "notes")]),
                ("feedback",
                 "Expert gives feedback to newbie on completed task.",
                 self.feedback,
                 [("rec", "recording name"),
                  ("assignee", "assignee"),
                  ("--notes", "notes")]),
                ("handover",
                 "Hand over recording to different assignee for next task.",
                 self.handover,
                 [("rec", "recording name"),
                  ("assignee", "assignee"),
                  ("--notes", "notes")]),
                ("reset",
                 "Cancel running tasks and checks, reset availability.",
                 self.reset,
                 [("rec", "recording name"),
                  ("--notes", "notes")]),
                ("create",
                 "First creation of a session, recording, or file.",
                 self.create,
                 [("--session", "session name"),
                  ("--rec", "recording name"),
                  ("--file", "file name"),
                  ("--notes", "notes")])
                ]:

            subparser = subparsers.add_parser(command, help=cmd_hlp)
            subparser.set_defaults(command=command, func=func)

            for name, arg_hlp in args:
                subparser.add_argument(name, help=arg_hlp)

        return parser

    def imp(self):
        """Import metadata from csv-files into database.

        Method will use class Import.
        """
        importer = Import(self.con, self.cur, self.args)
        importer.import_all()

    def exp(self):
        """Export metadata from the database to csv-files.

        Method will use class Export.
        """
        exporter = Export(self.con, self.cur, self.args)
        exporter.export_all()

    def send(self):
        print(self.args)
        print("Send command works!")

    def assign(self):
        print(self.args)
        print("Assign command works!")

    def update(self):
        print(self.args)
        print("Update command works!")

    def reassign(self):
        print(self.args)
        print("Reassign command works!")

    def letcheck(self):
        print(self.args)
        print("Letcheck command works!")

    def next(self):
        print(self.args)
        print("Next command works!")

    def feedback(self):
        print(self.args)
        print("Feedback command works!")

    def handover(self):
        print(self.args)
        print("Handover command works!")

    def checkin(self):
        print(self.args)
        print("Checkin command works!")

    def reset(self):
        print(self.args)
        print("Reset command works!")

    def create(self):
        print(self.args)
        print("Create command works!")


class ImpExp:
    """Base class for import and export class."""

    def __init__(self, con, cur, args):
        """Initialize database connection and cursor and cmd-line arguments."""
        self.con = con
        self.cur = cur
        self.args = args


class Export(ImpExp):
    """Class for exporting dene metadata from a MySQL database.

    Exports the following files to a directory called 'Export'
    (default path: current working directory):
        - sessions.csv
        - participants.csv
        - files.csv
        - file_locations.csv
        - monitor.csv

    The flag -p can be used to set the path of the 'Export' folder.
    """

    CSV_ATTRS = {
        "sessions": [
            "Code", "Date", "Location", "Length of recording",
            "Situation", "Content", "Participants and roles", "Comments"
            ],

        "participants": [
            "Short name", "Full name", "Birth date", "Age", "Gender",
            "Education", "First languages", "Second languages",
            "Main language", "Language biography", "Description",
            "Contact address", "E-mail/Phone"
            ],

        "files": [
            "Session code", "Recording code", "File name", "Type",
            "Format", "Duration", "Byte size", "Word size", "Location"
            ],

        "locations": [
            "File name", "CRDN", "FNUniv (project HD)", "UZH", "Notes"
            ],

        "monitor": [
            "recording name",	"quality", "child speech",
            "directedness", "Dene", "audio", "notes"
            ]
    }

    def __init__(self, con, cur, args):
        """Create 'Export' directory"""
        super().__init__(con, cur, args)

        # set path for 'Export' directory
        if self.args.path:
            self.path = os.path.join(self.args.path, "Export")
        else:
            self.path = "./Export"

        # create 'Export' directory
        if not os.path.isdir(self.path):
            try:
                os.mkdir(self.path)
            except FileNotFoundError:
                print("Export directory couldn't be created at", self.path)
                sys.exit(1)

    @classmethod
    def add_progress_fields(cls, tasks, fields, check_exceptions):
        """Add progress fields for monitor."""
        monitor = Export.CSV_ATTRS["monitor"]

        for task in tasks:
            # add task fields
            for field in fields:
                monitor.append(field + " " + task)
            # add check fields
            if task not in check_exceptions:
                for field in fields:
                    monitor.append(field + " check " + task)

    def get_hash(self, name, values):
        """Get hash for writing file."""
        return {Export.CSV_ATTRS[name][index]: value
                for index, value in enumerate(values)}

    def export_sessions(self):
        """Export to sessions.csv"""
        sessions_path = os.path.join(self.path, "sessions.csv")

        with open(sessions_path, "w") as sessions_file:

            sessions_writer = csv.DictWriter(
                sessions_file, fieldnames=Export.CSV_ATTRS["sessions"])
            sessions_writer.writeheader()

            # go through table 'sessions' in database
            self.cur.execute("SELECT * from sessions")
            for row in self.cur.fetchall():

                # get participants and roles for this session
                self.cur.execute("""
                    SELECT role, short_name FROM sessions_and_participants
                    JOIN participants
                    ON sessions_and_participants.participant_fk=participants.id
                    WHERE session_fk = {}
                    """.format(row["id"]))

                # create 'Participants and roles' string
                part_roles = ", ".join("{} ({})".format(
                    pair["short_name"],
                    " & ".join(role for role in pair["role"].split(",")))
                        for pair in self.cur)

                values = (row["name"], row["date"], row["location"],
                          row["situation"], row["duration"], row["content"],
                          row["notes"], part_roles)

                # write to sessions.csv
                sessions_writer.writerow(self.get_hash("sessions", values))

    def export_participants(self):
        """Export to participants.csv"""
        participants_path = os.path.join(self.path, "participants.csv")

        with open(participants_path, "w") as participants_file:

            participants_writer = csv.DictWriter(
                participants_file, fieldnames=Export.CSV_ATTRS["participants"])

            participants_writer.writeheader()

            # go through table 'participants' in database
            self.cur.execute("SELECT * FROM participants")
            for row in self.cur:

                values = (row["short_name"],
                          " ".join((row["first_name"], row["last_name"])),
                          row["birthdate"], row["age"], row["gender"],
                          row["education"], row["first_languages"],
                          row["second_languages"], row["main_language"],
                          row["language_biography"], row["description"],
                          row["contact_address"], row["email_phone"])

                # write to participants.csv
                participants_writer.writerow(self.get_hash("participants",
                                                           values))

    def export_files_locations(self):
        """Export to files.csv and file_locations.csv"""
        files_path = os.path.join(self.path, "files.csv")
        locations_path = os.path.join(self.path, "file_locations.csv")

        with open(files_path, "w") as files_file, \
                open(locations_path, "w") as locations_file:

            files_writer = csv.DictWriter(
                files_file, fieldnames=Export.CSV_ATTRS["files"])
            locations_writer = csv.DictWriter(
                locations_file, fieldnames=Export.CSV_ATTRS["locations"])

            files_writer.writeheader()
            locations_writer.writeheader()

            # go through table 'files' in database
            self.cur.execute("""
                SELECT files.*, recordings.name, sessions.name from files
                JOIN recordings ON files.recording_fk=recordings.id
                JOIN sessions ON recordings.session_fk=sessions.id""")

            for row in self.cur:

                values = (row["sessions.name"], row["recordings.name"],
                          row["name"], row["file_type"],
                          "/".join((row["file_type"], row["file_extension"])),
                          row["duration"], row["byte_size"], row["word_size"],
                          row["location"])

                # write to files.csv
                files_writer.writerow(self.get_hash("files", values))

                values = (row["name"], row["at_CRDN"], row["at_FNUniv"],
                          row["at_UZH"], row["notes"])

                # write to file_locations.csv
                locations_writer.writerow(self.get_hash("locations", values))

    def export_monitor(self):
        """Export to monitor.csv"""
        monitor_path = os.path.join(self.path, "monitor.csv")

        # add progress fields for monitor
        Export.add_progress_fields(
            ["segmentation", "transcription/translation", "glossing"],
            ["status", "person", "start", "end"],
            ["segmentation"]
        )

        with open(monitor_path, "w") as monitor_file:

            monitor_writer = csv.DictWriter(
                monitor_file, fieldnames=Export.CSV_ATTRS["monitor"])
            monitor_writer.writeheader()

            # go through table 'recordings' in database
            self.cur.execute("""
                SELECT recordings.*, first_name, last_name FROM recordings
                LEFT JOIN employees ON recordings.assignee_fk=employees.id""")

            for rec in self.cur.fetchall():

                values = (rec["name"], rec["overall_quality"],
                          rec["child_speech"], rec["directedness"],
                          rec["how_much_dene"], rec["audio_quality"],
                          rec["notes"])

                # inital content of dict
                monitor_dict = self.get_hash("monitor", values)

                self.get_progress_values(rec, monitor_dict)

                monitor_writer.writerow(monitor_dict)

    def get_progress_values(self, rec, monitor_dict):
        """Add progress values to monitor dictionary for a recording."""
        # check if someone is working on this recording
        if rec["availability"] == "assigned":
            # get assignee name
            assignee = rec["first_name"] + " " + rec["last_name"]
        else:
            assignee = ""

        self.cur.execute("""
            SELECT progress.*, name FROM progress
            JOIN task_types ON progress.task_type_fk=task_types.id
            WHERE progress.recording_fk={}
            """.format(rec["id"]))

        # go through those progress rows
        for progress in self.cur:
            # get task name
            task = progress["name"]
            # get status of this task
            monitor_dict["status " + task] = progress["task_status"]

            # get check status for this task except for 'segmentation'
            if task != "segmentation":
                monitor_dict["status check " + task] = \
                    progress["quality_check"]

            # if there's an assignee,
            # check if task or its check is in progress
            if assignee:
                for string, status in [("", progress["task_status"]),
                                       ("check ", progress["quality_check"])]:

                    if status == "in progress":
                        monitor_dict["person " + string + task] = assignee
                        break

    def export_all(self):
        self.export_sessions()
        self.export_participants()
        self.export_files_locations()
        self.export_monitor()
        print("Export finished!")


class Import(ImpExp):
    """Class for importing Dene metadata into a MySQL database.

    For a full import the following files are used:
        - sessions.csv
        - participants.csv
        - files.csv
        - file_locations.csv
        - monitor.csv

    The import populates the following tables:
        - sessions
        - participants
        - sessions_and_participants
        - recordings
        - progress
        - files

    Optionally the flag -d can be set, if there should be a 'radical' import
    which means that all existing rows in the database are deleted first
    before all records are inserted again from the files.
    """

    DB_ATTRS = {

        "action_log": [
            "time", "action_fk", "recording_fk", "file_fk", "task_type_fk",
            "client_fk", "assignee_fk", "notes"],

        "files": [
            "name", "recording_fk", "file_type", "file_extension",
            "duration", "byte_size", "word_size", "at_UZH", "at_FNUniv",
            "at_CRDN", "location", "notes"
            ],

        "participants": [
            "short_name", "first_name", "last_name", "birthdate", "age",
            "gender", "education", "first_languages", "second_languages",
            "main_language", "language_biography", "description",
            "contact_address", "email_phone"
            ],

        "progress": [
            "recording_fk", "task_type_fk", "task_status",
            "quality_check", "notes"
            ],

        "recordings": [
            "name", "session_fk", "availability", "assignee_fk",
            "overall_quality", "child_speech", "directedness",
            "how_much_dene", "audio_quality", "notes"
            ],

        "sessions": [
            "name", "date", "location", "duration",
            "situation", "content", "notes"
            ],

        "sessions_and_participants": [
            "session_fk", "participant_fk", "role"
            ]
    }

    class ID:
        """Class providing methods for getting IDs"""

        def __init__(self, outer_class):
            self.importer = outer_class

        def get_id(self, cmd, error_msg):
            """Get id of some table"""
            self.importer.cur.execute(cmd)
            try:
                id = self.importer.cur.fetchone()[0]
            except TypeError:
                self.importer.logger.error(error_msg)
                return None

            return id

        def get_assignee(self, assignee):
            """Get id of an assignee"""
            cmd = """SELECT id FROM employees
                     WHERE CONCAT(first_name, ' ', last_name) = '{}'
                  """.format(assignee)
            error_msg = """Assignee '{}' not in table 'employees'
                        """.format(assignee)

            return self.get_id(cmd, error_msg)

        def get_session(self, rec):
            """Get session code from recording name"""
            try:
                # try to extract session code from recording code
                regex = r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d+)?"
                session_code = re.search(regex, rec).group()
            except AttributeError:
                self.logger.error(
                    "Session code cannot be extracted from recording code",
                    rec)
                return None

            cmd = """SELECT id FROM sessions WHERE name = '{}'
                  """.format(session_code)
            error_msg = """Session code '{}' not in table 'sessions'
                        """.format(session_code)

            return self.get_id(cmd, error_msg)

        def get_action(self, action):
            """Get id of an action name"""
            cmd = "SELECT id FROM actions WHERE action = '{}'".format(action)
            error_msg = "Action '{}' not in table 'actions' ".format(action)

            return self.get_id(cmd, error_msg)

        def get_task_type(self, task_type):
            """Get id of a task type"""
            cmd = """SELECT id FROM task_types WHERE name = '{}'
                  """.format(task_type)
            error_msg = """Task type '{}' not in table 'task_types'
                        """.format(task_type)

            return self.get_id(cmd, error_msg)

        def get_rec(self, rec):
            """Get id of a recording"""
            cmd = "SELECT id from recordings WHERE name = '{}'".format(rec)
            error_msg = """Recording name '{}' not in table 'recordings'
                        """.format(rec)

            return self.get_id(cmd, error_msg)

        def get_participant(self, shortname):
            """Get id of a participant"""
            cmd = """SELECT id FROM participants WHERE short_name = '{}'
                  """.format(shortname)
            error_msg = """Short name '{}' not in table 'participants'
                        """.format(shortname)

            return self.get_id(cmd, error_msg)

    def __init__(self, con, cur, args):
        """Get logger and ID-getter."""
        super().__init__(con, cur, args)

        self.logger = self.get_logger()
        self.id = self.ID(self)

        # turn MySQLdb warnings into errors,
        # so that they can be caught by exceptions and be logged
        warnings.filterwarnings("error", category=MySQLdb.Warning)

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
            self.cur.execute("""ALTER TABLE {} NOCHECK CONSTRAINT all
                             """.format(associated_table))
            self.con.commit()

        # delete all rows
        self.cur.execute("DELETE FROM {};".format(table))
        self.con.commit()

        # enable foreign key checks again in all tables linked to this table
        for associated_table in associated_tables:
            self.cur.execute("""ALTER TABLE {} CHECK CONSTRAINT all
                             """.format(associated_table))
            self.con.commit()

        # set auto-incrementing to 1
        self.cur.execute("""ALTER TABLE {} AUTO_INCREMENT = 1""".format(table))
        self.con.commit()

    def empty_str_to_none(self, row):
        """Set all empty strings to None"""
        for field in row:
            if not row[field]:
                row[field] = None

    def execute(self, cmd, values, table, key=""):
        """Execute SQL commands and log any SQL errors.

        args:
            cmd:
                (ideally) an insert or/and update SQL command
            values:
                values to be inserted/updated
            table:
                for logging, specify table into which values are to be inserted
            key:
                for logging, specify some identfier for the record
                to be inserted (e.g. session code)
        """
        counter = 0

        try:
            self.cur.execute(cmd, values)
        except db.Error as e:
            self.logger.error("{}|{}|{}".format(repr(e), table, key))
            counter += 1

        self.con.commit()

        return counter

    def get_insertupdate_cmd(self, table):
        """Create INSERT/UPDATE command.

        Command updates values if a record already exists,
        otherwise it inserts a new record.
        """
        db_attributes = Import.DB_ATTRS[table]

        return """INSERT INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE {}
               """.format(
                    table,
                    ",".join(db_attributes),
                    ",".join("%s" for attr in db_attributes),
                    ','.join((attr + "=%s") for attr in db_attributes)
                    )

    def import_sessions(self):
        """Populate table 'sessions' by import from sessions.csv"""
        # try reading sessions.csv
        try:
            sessions_file = open(self.args.sessions, "r")
        except FileNotFoundError:
            print("Path to sessions.csv not correct! No import possible!")
            return

        # get command for inserting/updating session records
        cmd = self.get_insertupdate_cmd("sessions")

        # number of sessions not imported
        counter = 0

        # go through each session in sessions.csv
        for s in tqdm(csv.DictReader(sessions_file),
                      desc="Reading from sessions.csv", unit=" sessions"):

            self.empty_str_to_none(s)

            values = 2*(
                s["Code"], s["Date"], s["Location"], s["Length of recording"],
                s["Situation"], s["Content"], s["Comments"]
            )

            counter += self.execute(cmd, values, "sessions", s["Code"])

            # link session to participants
            self.link_sessions_participants(s["Participants and roles"],
                                            s["Code"])

        sessions_file.close()

        print(counter, "sessions not imported")
        sys.stdout.flush()

    def link_sessions_participants(self, participants_roles, session_code):
        """Populate table 'sessions_and_participants'."""
        session_id = self.id.get_session(session_code)

        # if participants and roles is not empty and session code is not null
        if participants_roles and session_id:

            # go through participants and their roles
            for part_roles in participants_roles.split(", "):

                # try to extract shortname and its roles
                try:
                    shortname, roles = re.split(r" (?=\()", part_roles)
                    # strip braces around role(s)
                    roles = roles[1:-1]
                except ValueError:
                    self.logger.error(
                        "Format of Participants and roles not correct|"
                        + session_code)
                    continue

                # create set of roles
                role_set = set(roles.split(" & "))

                participant_id = self.id.get_participant(shortname)
                if participant_id is None:
                    continue

                cmd = self.get_insertupdate_cmd("sessions_and_participants")

                values = 2*(session_id, participant_id, role_set)

                self.execute(cmd, values, "sessions/participants",
                             key="{}/{}".format(session_code, shortname))

    def import_participants(self):
        """Populate table 'participants' by import from participants.csv"""
        # try reading participants.csv
        try:
            participants_file = open(self.args.participants, "r")
        except FileNotFoundError:
            print("Path to participants.csv not correct! No import possible!")
            return

        # get command for inserting/updating participant records
        cmd = self.get_insertupdate_cmd("participants")

        # number of participants not imported
        counter = 0

        # go through each participant in participants.csv
        for p in tqdm(csv.DictReader(participants_file),
                      desc="Reading from participants.csv",
                      unit=" participants"):

            self.empty_str_to_none(p)

            # extract first-/lastname assuming that
            # only the firstname can consist of more than one word
            # TODO: make this more foolproof?
            try:
                *first_name, last_name = p["Full name"].split()
            except Exception:
                first_name = None
                last_name = None
            else:
                first_name = " ".join(first_name)

            # create sets for language fields that have more than one value
            for field in ["Main language", "First languages",
                          "Second languages"]:
                if p[field] is not None:
                    p[field] = set(p[field].split("/"))

            values = 2*(
                p["Short name"], first_name, last_name, p["Birth date"],
                p["Age"], p["Gender"], p["Education"], p["First languages"],
                p["Second languages"], p["Main language"],
                p["Language biography"], p["Description"],
                p["Contact address"], p["E-mail/Phone"]
            )

            counter += self.execute(cmd, values, "participants",
                                    p["Short name"])

        participants_file.close()

        print(counter, "participants not imported")
        sys.stdout.flush()

    def import_monitor(self):
        """Populate tables 'recordings' and'progress'.

        By import from monitor.csv.
        """
        # try reading monitor.csv
        try:
            monitor_file = open(self.args.monitor, "r")
        except FileNotFoundError:
            print("Path to monitor.csv not correct! Import not possible!")
            return

        recordings_cmd = self.get_insertupdate_cmd("recordings")
        progress_cmd = self.get_insertupdate_cmd("progress")
        action_log_cmd = self.get_insertupdate_cmd("action_log")

        # number of recordings not imported
        counter = 0

        # go through each recording in database
        for rec in tqdm(csv.DictReader(monitor_file),
                        desc="Reading from monitor.csv", unit=" recordings"):

            self.empty_str_to_none(rec)

            # try to get session id
            session_id = self.id.get_session(rec["recording name"])
            if session_id is None:
                counter += 1
                continue

            # assignee for a recording
            rec_assignee_id = None
            # default value for availability of a recording
            availability = "free"
            # action logs for a recording
            action_logs = []

            # TODO: disentangle recordings and action logs (like for progress)
            # to improve readability? But performance might be a bit worse...

            # go through the tasks
            for task in ["segmentation", "transcription/translation",
                         "glossing"]:

                # go through task and check fields
                # and collect values for tables 'recordings' and 'action_log'
                for is_check, field in [(False, task),
                                        (True, "check " + task)]:

                    # ignore segmentation check field
                    if is_check and task == "segmentation":
                        continue

                    # get status field
                    status = rec["status " + field]

                    is_in_progress = status == "in progress"
                    is_complete = status == "complete" \
                        or status == "incomplete"

                    if status == "defer" or status == "barred":
                        availability = status
                    elif is_in_progress or is_complete:
                        # get person field
                        person = rec["person " + field]

                        # get task and assignee id
                        task_type_id = self.id.get_task_type(task)
                        assignee_id = self.id.get_assignee(person)

                        if is_in_progress:
                            availability = "assigned"
                            rec_assignee_id = assignee_id

                        # get appropriate 'start' action
                        if is_check:
                            action_id = self.id.get_action("letcheck")
                        else:
                            action_id = self.id.get_action("assign")

                        # if all id's could be fetched
                        if assignee_id and task_type_id and action_id:

                            # add to action_logs list
                            action_logs.append([
                                rec["start " + field], action_id, None, None,
                                task_type_id, None, assignee_id, None])

                            if is_complete:
                                # add additional log with checkin action
                                action_id = self.id.get_action("checkin")
                                if action_id:
                                    action_logs.append([
                                        rec["end " + field], action_id, None,
                                        None, task_type_id, None,
                                        assignee_id, None])

            # skip if a recording is assigned but there is no assignee (id)
            if availability == "assigned" and not rec_assignee_id:
                counter += 1
                continue

            # insert recording

            rec_values = 2*(
                rec["recording name"], session_id, availability,
                rec_assignee_id, rec["quality"], rec["child speech"],
                rec["directedness"], rec["Dene"], rec["audio"], rec["notes"]
            )

            counter += self.execute(recordings_cmd, rec_values, "recordings",
                                    rec["recording name"])

            # get id of just imported recording
            rec["id"] = self.id.get_rec(rec["recording name"])
            if rec["id"] is None:
                continue

            # populate tables action_log and progress
            self.fill_action_log(action_log_cmd, action_logs, rec)
            self.fill_progress(progress_cmd, rec)

        monitor_file.close()

        print(counter, "recordings not imported")
        sys.stdout.flush()

    def fill_action_log(self, action_log_cmd, action_logs, rec):
        """Insert or update action logs for a recording"""
        # insert/update actions of a recording to action_log
        for action_values in action_logs:
            # add recording id
            action_values[2] = rec["id"]
            self.execute(action_log_cmd, 2*action_values, "action_log",
                         rec["recording name"])

    def fill_progress(self, progress_cmd, rec):
        """Insert or update progress records for a recording"""
        # go through each task type from monitor.csv
        for task in ["segmentation", "transcription/translation", "glossing"]:

            task_type_id = self.id.get_task_type(task)

            if task_type_id is None:
                continue

            # get status of this task
            task_status = rec["status " + task]

            if task_status == "barred" or task_status == "defer":
                task_status = "not started"

            if task == "segmentation":
                quality_check = "not required"
            else:
                quality_check = rec["status check " + task]

            progress_values = 2*(rec["id"], task_type_id, task_status,
                                 quality_check, None)

            self.execute(progress_cmd, progress_values,
                         "progress", rec["recording name"])

    def import_files(self):
        """Populate table 'files'.

        By import from files.csv and file_locations.csv.
        """
        # try reading files.csv
        try:
            files_file = open(self.args.files, "r")
        except FileNotFoundError:
            print("Path to files.csv not correct! Import not possible!")
            return

        # try reading file_locations.csv
        try:
            locations_file = open(self.args.locations, "r")
        except FileNotFoundError:
            print("Path to file_locations.csv not correct! "
                  + "Import not possible!")
            return

        # store metadata of file_locations.csv for fast retrieval
        locations = {}
        for file in csv.DictReader(locations_file):
            locations[file["File name"]] = {
                "at_UZH": file["UZH"],
                "at_FNUniv": file["FNUniv (project HD)"],
                "at_CRDN": file["CRDN"],
                "notes": file["Notes"]}

        locations_file.close()

        cmd = self.get_insertupdate_cmd("files")

        # number of files not imported
        counter = 0

        for file in tqdm(csv.DictReader(files_file),
                         desc="Reading from files.csv", unit=" files"):

            self.empty_str_to_none(file)

            rec_id = self.id.get_rec(file["Recording code"])
            if rec_id is None:
                counter += 1
                continue

            # try to get the locations of this file
            try:
                loc = locations[file["File name"]]
            except KeyError:
                self.logger.error("""File '{}' not in 'file_locations.csv'
                                  """.format(file["File name"]))
                counter += 1
                continue

            file_type = file["Type"].lower()

            # media files: no versions, thus only 'no' and 'latest version'
            if file_type == "video" or file_type == "audio":

                for field in ["at_UZH", "at_FNUniv", "at_CRDN"]:

                    if "yes" in loc[field]:
                        loc[field] = "latest version"
                    else:
                        loc[field] = "no"

            # TODO: textual files

            values = 2*(
                file["File name"], rec_id, file["Type"].lower(),
                file["Format"][-3:], file["Duration"], file["Byte size"],
                file["Word size"], loc["at_UZH"], loc["at_FNUniv"],
                loc["at_CRDN"], file["Location"], loc["notes"]
            )

            counter += self.execute(cmd, values, "files", file["File name"])

        files_file.close()

        print(counter, "files not imported")
        sys.stdout.flush()

    def import_all(self):
        """Import from all files"""
        if self.args.radical:

            # TODO: action log must not (!) be completely deleted
            # -> only actions that can be read from monitor:
            # assign, letcheck, checkin

            # delete all rows from all tables
            for table in ["action_log", "files", "sessions_and_participants",
                          "progress", "recordings", "sessions", "participants"
                          ]:

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
        print()
        print("See db.log for a detailed error report")


def main():
    """Start database interface application"""
    with DB_Manager(host="localhost", user="anna", passwd="anna",
                    database="deslas") as manager:
        manager.start()


if __name__ == '__main__':
    main()
