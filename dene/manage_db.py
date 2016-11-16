"""Module providing classes for interacting with the Dene database.

This module can be used to manipulate the database over the terminal by using
one of the following commands: import, export, send, assign, update, reassign,
checkin, letcheck, feedback, handover, reset, create.
For more details on these commands run like this:
    python3 db_manager.py [command] --help

The following external python modules (which can be installed by pip) are used:
    - mysqlclient (interface to MySQL)
    - tqdm (progress meter)
"""

import os
import re
import abc
import sys
import csv
import logging
import warnings
import argparse

from datetime import datetime, timedelta

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


class DBInterface:
    """Interface for working with the Dene database."""

    db_credentials = {"host": "mysqlprod01.uzh.ch",
                      "user": "deslas",
                      "passwd": "",
                      "db": "deslas",
                      "charset": "utf8"}

    def run(self):
        """Start main application.

        Command line arguments are parsed to determine action to be taken.
        """
        # get command line parser
        parser = self.get_parser()
        # parse all of its arguments and store them
        self.args = parser.parse_args()

        # execute appropriate action
        with self.args.cls(self.args, **self.db_credentials) as action:
            action.start()

    def get_parser(self):
        """Get command line parser."""
        # TODO: make method shorter or more modular?

        # get main parser
        parser = argparse.ArgumentParser()
        # add subparsers that will hold the subcommands
        subparsers = parser.add_subparsers()

        # add subcommand 'import'
        import_parser = subparsers.add_parser(
            "import", help="Import metadata from csv files to database")
        import_parser.set_defaults(command="import", cls=Import)

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
        checkin_parser.set_defaults(command="checkin", cls=Checkin)

        checkin_parser.add_argument("file", help="file name")
        checkin_parser.add_argument("status", help="set task status",
                                    choices=["complete", "incomplete"])
        checkin_parser.add_argument("--checked", help="task is checked",
                                    action="store_true")
        checkin_parser.add_argument("--notes", help="notes")

        # add all other subcommands
        for command, cmd_hlp, cls, args in [
                ("export",
                 "Export metadata from database to csv files",
                 Export,
                 [("--path", "directory path where files are saved")]),
                ("send",
                 "Send latest version of a file to a person.",
                 Send,
                 [("file", "file name"),
                  ("recipient", "recipient"),
                  ("--notes", "notes")]),
                ("assign",
                 "Assign recording to a person for a task.",
                 Assign,
                 [("rec", "recording name"),
                  ("assignee", "assignee"), ("task", "task"),
                  ("--notes", "notes")]),
                ("update",
                 "Upload new version of file"
                 + "without changing workflow status.",
                 Update,
                 [("file", "file name"),
                  ("--notes", "notes")]),
                ("reassign",
                 "Assign running task to a different person.",
                 Reassign,
                 [("rec", "recording name"),
                  ("assignee", "assignee"),
                  ("--notes", "notes")]),
                ("letcheck",
                 "Assign recording to specialist for feedback.",
                 Letcheck,
                 [("rec", "recording name"),
                  ("assignee", "assignee"),
                  ("--notes", "notes")]),
                ("next",
                 "Have same assignee do the next task"
                 + "in the predefined order.",
                 Next,
                 [("rec", "recording name"),
                  ("--notes", "notes")]),
                ("feedback",
                 "Expert gives feedback to newbie on completed task.",
                 Feedback,
                 [("rec", "recording name"),
                  ("assignee", "assignee"),
                  ("--notes", "notes")]),
                ("handover",
                 "Hand over recording to different assignee for next task.",
                 Handover,
                 [("rec", "recording name"),
                  ("assignee", "assignee"),
                  ("--notes", "notes")]),
                ("reset",
                 "Cancel running tasks and checks, reset availability.",
                 Reset,
                 [("rec", "recording name"),
                  ("--notes", "notes")]),
                ("create",
                 "First creation of a session, recording, or file.",
                 Create,
                 [("--session", "session name"),
                  ("--rec", "recording name"),
                  ("--file", "file name"),
                  ("--notes", "notes")])
                ]:

            subparser = subparsers.add_parser(command, help=cmd_hlp)
            subparser.set_defaults(command=command, cls=cls)

            for name, arg_hlp in args:
                subparser.add_argument(name, help=arg_hlp)

        return parser


class Action(metaclass=abc.ABCMeta):
    """Abstract base class for all action types."""

    def __init__(self, args, dict_cur=False, **db_credentials):
        """Initialize database connection/cursor and cmd-line arguments."""
        self.con = db.connect(**db_credentials)

        if dict_cur:
            self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)
        else:
            self.cur = self.con.cursor()

        self.args = args

    def __enter__(self):
        """Return class object."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close database cursor and connection."""
        self.cur.close()
        self.con.close()

    @abc.abstractmethod
    def start(self):
        pass


class Send(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Send command works!")


class Assign(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Assign command works!")


class Update(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Update command works!")


class Reassign(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Reassign command works!")


class Letcheck(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Letcheck command works!")


class Next(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Next command works!")


class Feedback(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Feedback command works!")


class Handover(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Handover command works!")


class Checkin(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Checkin command works!")


class Reset(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Reset command works!")


class Create(Action):
    """Add doc."""
    def start(self):
        print(self.args)
        print("Create command works!")


class Export(Action):
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

    csv_attrs = {
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

    def __init__(self, args, **db_credentials):
        """Create 'Export' directory."""
        super().__init__(args, dict_cur=True, **db_credentials)

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

    @staticmethod
    def get_progress_fields(tasks, fields, check_exceptions):
        """Get progress fields."""
        progress = []

        for task in tasks:
            # add task fields
            for field in fields:
                progress.append(field + " " + task)
            # add check fields
            if task not in check_exceptions:
                for field in fields:
                    progress.append(field + " check " + task)

        return progress

    def get_hash(self, name, values):
        """Get hash for writing file."""
        return {self.csv_attrs[name][index]: value
                for index, value in enumerate(values)}

    def export_sessions(self):
        """Export to sessions.csv"""
        sessions_path = os.path.join(self.path, "sessions.csv")

        with open(sessions_path, "w") as sessions_file:

            sessions_writer = csv.DictWriter(
                sessions_file, fieldnames=self.csv_attrs["sessions"])
            sessions_writer.writeheader()

            # go through table 'sessions' in database
            self.cur.execute("SELECT * FROM sessions")
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
                          row["duration"], row["situation"], row["content"],
                          part_roles, row["notes"])

                # write to sessions.csv
                sessions_writer.writerow(self.get_hash("sessions", values))

    def export_participants(self):
        """Export to participants.csv."""
        participants_path = os.path.join(self.path, "participants.csv")

        with open(participants_path, "w") as participants_file:

            participants_writer = csv.DictWriter(
                participants_file, fieldnames=self.csv_attrs["participants"])

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
        """Export to files.csv and file_locations.csv."""
        files_path = os.path.join(self.path, "files.csv")
        locations_path = os.path.join(self.path, "file_locations.csv")

        with open(files_path, "w") as files_file, \
                open(locations_path, "w") as locations_file:

            files_writer = csv.DictWriter(
                files_file, fieldnames=self.csv_attrs["files"])
            locations_writer = csv.DictWriter(
                locations_file, fieldnames=self.csv_attrs["locations"])

            files_writer.writeheader()
            locations_writer.writeheader()

            # go through table 'files' in database
            self.cur.execute("""
                SELECT files.*, recordings.name, sessions.name FROM files
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

                for field in ["at_CRDN", "at_FNUniv", "at_UZH"]:
                    if row[field] == "latest version":
                        row[field] = "yes"
                    else:
                        row[field] = "no"

                values = (row["name"], row["at_CRDN"], row["at_FNUniv"],
                          row["at_UZH"], row["notes"])

                # write to file_locations.csv
                locations_writer.writerow(self.get_hash("locations", values))

    def export_monitor(self):
        """Export to monitor.csv."""
        monitor_path = os.path.join(self.path, "monitor.csv")

        # get progress fields for monitor
        progress = self.get_progress_fields(
            ["segmentation", "transcription/translation", "glossing"],
            ["status", "person", "start", "end"],
            ["segmentation"]
        )

        with open(monitor_path, "w") as monitor_file:

            monitor_writer = csv.DictWriter(
                monitor_file, fieldnames=self.csv_attrs["monitor"] + progress)
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

                # add progress fields (initialized as empty strings) to dict
                for field in progress:
                    monitor_dict[field] = ""

                self.get_progress_values(rec, monitor_dict)

                monitor_writer.writerow(monitor_dict)

    def get_progress_values(self, rec, monitor_dict):
        """Add progress values to monitor dictionary for a recording."""
        # get progress records associated with this recording
        self.cur.execute("""
            SELECT progress.*, name FROM progress
            JOIN task_types ON progress.task_type_fk=task_types.id
            WHERE progress.recording_fk={}
            """.format(rec["id"]))

        # go through those progress rows
        for progress in self.cur.fetchall():
            # get task name
            task = progress["name"]
            # get status of this task
            monitor_dict["status " + task] = progress["task_status"]

            # get check status for this task (except for segmentation)
            if task != "segmentation":
                monitor_dict["status check " + task] = \
                    progress["quality_check"]

            # get data from action log for this recording and task type
            self.cur.execute("""
                SELECT time, actions.action, recordings.name, task_types.name,
                employees.first_name, employees.last_name FROM action_log
                JOIN actions ON action_log.action_fk=actions.id
                JOIN recordings ON action_log.recording_fk=recordings.id
                JOIN task_types ON action_log.task_type_fk=task_types.id
                JOIN employees ON action_log.assignee_fk=employees.id
                WHERE action_log.recording_fk={} and action_log.task_type_fk={}
                """.format(rec["id"], progress["task_type_fk"]))

            # get all actions of this recording sorted by time and action
            actions = sorted(
                [(log["action"], log["time"],
                  log["first_name"] + " " + log["last_name"])
                 for log in self.cur],
                key=lambda x: (x[1], x[0]))

            assign_found = False
            letcheck_found = False

            for index in range(len(actions)):
                action = actions[index][0]

                # find first assign
                if not assign_found and action == "assign":
                    assign_found = True
                    monitor_dict["start " + task] = actions[index][1]
                    monitor_dict["person " + task] = actions[index][2]

                # find first letcheck
                if not letcheck_found and action == "letcheck":
                    letcheck_found = True
                    monitor_dict["start check " + task] = actions[index][1]
                    monitor_dict["person check " + task] = actions[index][2]

                # find last checkins
                if action == "checkin":
                    previous_action = actions[index - 1][0]

                    # checkin for task
                    if previous_action == "assign":
                        monitor_dict["end " + task] = actions[index][1]
                    # checkin for task check
                    elif previous_action == "letcheck":
                        monitor_dict["end check " + task] = actions[index][1]

        # if availability is 'defer' or 'barred', find out which task it is
        # and set this status for this task
        if rec["availability"] in ["defer", "barred"]:

            for task in ["segmentation", "transcription/translation",
                         "glossing"]:

                if monitor_dict["status " + task] == "not started":
                    monitor_dict["status " + task] = rec["availability"]
                    break
                elif (task != "segmentation" and
                      monitor_dict["status check " + task] == "not started"):

                    monitor_dict["status check " + task] = rec["availability"]
                    break

    def start(self):
        self.export_sessions()
        self.export_participants()
        self.export_files_locations()
        self.export_monitor()
        print("Export finished!")
        print()


class Import(Action):
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

    db_attrs = {

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
        """Class providing methods for getting IDs."""

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

        def get_assignee(self, assignee, task="", rec_name="", func=""):
            """Get id of an assignee.

            task (string):
                name of the task, for logging
            rec_name (string):
                name of the recording, for logging
            func (string):
                name of function that called this function, for logging
            """
            # check if assignee name is not empty or null
            if not assignee:
                self.importer.logger.error(
                    """Assignee of task {} for recording {}
                       is missing|{}""".format(task, rec_name, func))
                return None

            cmd = """SELECT id FROM employees
                     WHERE CONCAT(first_name, ' ', last_name) = '{}'
                  """.format(assignee)
            error_msg = """Assignee '{}' not in table 'employees'|{}
                        """.format(assignee, func)

            return self.get_id(cmd, error_msg)

        def get_session(self, name, isrec=False, func=""):
            """Get id of a session.

            isrec (boolean):
                specify if a recording or session name is given
            func (string):
                name of function that called this function, for logging
            """
            if isrec:
                try:
                    # try to extract session code from recording code
                    regex = r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d+)?"
                    session_code = re.search(regex, name).group()
                except AttributeError:
                    self.logger.error(
                        "Session code cannot be extracted from recording code "
                        + name)
                    return None
            else:
                session_code = name

            cmd = """SELECT id FROM sessions WHERE name = '{}'
                  """.format(session_code)
            error_msg = """Session code '{}' not in table 'sessions|{}'
                        """.format(session_code, func)

            return self.get_id(cmd, error_msg)

        def get_action(self, action):
            """Get id of an action name."""
            cmd = "SELECT id FROM actions WHERE action = '{}'".format(action)
            error_msg = "Action '{}' not in table 'actions' ".format(action)

            return self.get_id(cmd, error_msg)

        def get_task_type(self, task_type):
            """Get id of a task type."""
            cmd = """SELECT id FROM task_types WHERE name = '{}'
                  """.format(task_type)
            error_msg = """Task type '{}' not in table 'task_types'
                        """.format(task_type)

            return self.get_id(cmd, error_msg)

        def get_rec(self, rec, func=""):
            """Get id of a recording.

            func (string):
                name of function that called this function, for logging
            """
            cmd = "SELECT id from recordings WHERE name = '{}'".format(rec)
            error_msg = """Recording name '{}' not in table 'recordings'|{}
                        """.format(rec, func)

            return self.get_id(cmd, error_msg)

        def get_participant(self, shortname):
            """Get id of a participant."""
            cmd = """SELECT id FROM participants WHERE short_name = '{}'
                  """.format(shortname)
            error_msg = """Short name '{}' not in table 'participants'
                        """.format(shortname)

            return self.get_id(cmd, error_msg)

    def __init__(self, args, **db_credentials):
        """Get logger and ID-getter."""
        super().__init__(args, **db_credentials)

        self.logger = self.get_logger()
        self.id = self.ID(self)

        # turn MySQLdb warnings into errors,
        # so that they can be caught by exceptions and be logged
        warnings.filterwarnings("error", category=MySQLdb.Warning)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close and remove file handler."""
        super().__exit__(exc_type, exc_value, exc_traceback)

        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
            handler.flush()
            handler.close()

    def get_logger(self):
        """Produce logs if database errors occur."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler("db.log", mode="w")
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(funcName)s|%(levelname)s|%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def wipe(self, table, associated_tables=[]):
        """Delete all rows of a table."""
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
        """Set all empty strings to None."""
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
        has_error = 0

        try:
            self.cur.execute(cmd, values)
        except db.Error as e:
            self.logger.error("{}|{}|{}".format(repr(e), table, key))
            has_error = 1

        self.con.commit()

        return has_error

    def get_insertupdate_cmd(self, table):
        """Create INSERT/UPDATE command.

        Command updates values if a record already exists,
        otherwise it inserts a new record.
        """
        db_attributes = self.db_attrs[table]

        return """INSERT INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE {}
               """.format(
                    table,
                    ",".join(db_attributes),
                    ",".join("%s" for attr in db_attributes),
                    ','.join((attr + "=%s") for attr in db_attributes)
                    )

    def import_sessions(self):
        """Populate table 'sessions' by import from sessions.csv."""
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
        session_id = self.id.get_session(session_code,
                                         func="link_sessions_participants")

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
        """Populate table 'participants' by import from participants.csv."""
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

        # go through each recording in monitor.csv
        for rec in tqdm(csv.DictReader(monitor_file),
                        desc="Reading from monitor.csv", unit=" recordings"):

            self.empty_str_to_none(rec)

            self.clean_up_monitor(rec)

            # get recording name
            rec_name = rec["recording name"]

            # track if there are errors for this recording
            has_error = 0

            # get all values for this recording
            rec_values = self.get_rec_values(rec)

            if rec_values is None:
                counter += 1
                continue

            # insert recording
            has_error = self.execute(recordings_cmd, rec_values,
                                     "recordings", rec_name)

            # get id of just imported recording and add to rec hash if no error
            if has_error:
                counter += 1
                continue
            else:
                rec["id"] = self.id.get_rec(rec_name, func="import_monitor")

            # get progress records and action logs for this recording
            progress_records = self.get_progress_values(rec)
            action_logs = self.get_action_log_values(rec)

            if progress_records is None or action_logs is None:
                has_error = 1

            # insert progress records if there are no previous errors
            if not has_error:
                for progress in progress_records:
                    has_error = self.execute(progress_cmd, progress,
                                             "progress", rec_name)
                    if has_error:
                        break

            # insert action logs if there are no previous errors
            if not has_error:
                for action_log in action_logs:
                    has_error = self.execute(action_log_cmd, action_log,
                                             "action_log", rec_name)
                    if has_error:
                        break

            # if anything went wrong until here
            # delete every item in the database associated with this recording
            if has_error:
                # first delete action logs and progress records associated
                # with this recording
                for table in ["action_log", "progress"]:
                    self.cur.execute(
                        "DELETE FROM {} WHERE recording_fk='{}'".format(
                            table, rec["id"]))
                    self.con.commit()

                # then delete recording itself
                self.cur.execute(
                    "DELETE FROM recordings WHERE id = '{}'".format(rec["id"]))
                self.con.commit()

                counter += 1

        monitor_file.close()

        print(counter, "recordings not imported")
        sys.stdout.flush()

    def clean_up_monitor(self, rec):
        """Do some cleaning up before importing monitor data.

        Assign specific dates/times for missing start and end fields.
        Unknown dates always get the time '23:59:59'.
        Unknown task starts get the date '1111-11-11'.
        Unknown task ends get the date from the task start.
        Unknown check starts get the date from the task end.
        Unknown check ends get the date from check start + 1 day
        """
        def get_dt(date, obj=False):
            """Helper function for creating dates that are unknown."""

            formats = ["%Y-%m-%d", "%Y.%m.%d", "%Y-%m-%d %H:%M:%S",
                       "%Y.%m.%d %H:%M:%S"]

            for frmt in formats:
                try:
                    dt = datetime.strptime(date, frmt)
                except ValueError:
                    pass
                else:
                    dt = dt.replace(hour=23, minute=59, second=59)

                    if obj:
                        return dt
                    else:
                        return dt.strftime("%Y-%m-%d %H:%M:%S")

        # possible values for unknown dates
        empty_values = ["", "-", "?", None]

        for task in ["segmentation", "transcription/translation", "glossing"]:

            task_status = rec["status " + task]

            if task_status in ["complete", "incomplete", "in progress"]:

                if rec["start " + task] in empty_values:
                    rec["start " + task] = "1111-11-11 23:59:59"

                if task_status in ["complete", "incomplete"]:

                    if rec["end " + task] in empty_values:
                        rec["end " + task] = get_dt(rec["start " + task])

            if task != "segmentation":
                check_status = rec["status check " + task]

                if check_status in ["complete", "incomplete", "in progress"]:

                    if rec["start check " + task] in empty_values:
                        rec["start check " + task] = get_dt(rec["end " + task])

                    if check_status in ["complete", "incomplete"]:

                        if rec["end check " + task] in empty_values:

                            # add one day to avoid dupblicates since two
                            # different checkins are possible:
                            # after assign and letcheck
                            org_date = get_dt(rec["start check " + task],
                                              obj=True)

                            rec["end check " + task] = \
                                org_date + timedelta(days=1)

    def get_rec_values(self, rec):
        """Insert or update recordings."""
        # get recording name
        rec_name = rec["recording name"]
        # get session id
        session_id = self.id.get_session(rec_name, isrec=True,
                                         func="get_rec_values")
        if session_id is None:
            return None

        # default values
        availability = "free"
        assignee_id = None

        # find out availability and assignee id for a recording by iterating
        # through monitor fields backwards and break loop as soon one of the
        # following status's is found: 'in progress', 'defer' or 'barred'
        # and overwrite the default values for availability and assignee
        for task in ["glossing", "transcription/translation", "segmentation"]:

            # get task status and assignee
            task_status = rec["status " + task]
            task_assignee = rec["person " + task]

            # get check status and assignee
            # additionally check if task has a check field
            if task == "segmentation":
                check_status = None
                check_assignee = None
            else:
                check_status = rec["status check " + task]
                check_assignee = rec["person check " + task]

            # overwrite default values for availability and assignee if status
            # is 'in progress'; if status is 'defer' or 'barred'
            # only overwrite availability
            if check_status == "in progress":
                availability = "assigned"
                assignee_id = self.id.get_assignee(
                    check_assignee, task=task + "/check",
                    rec_name=rec_name, func="get_rec_values")
                if assignee_id is None:
                    return None
                break
            elif check_status in ["defer", "barred"]:
                availability = check_status
                break
            elif task_status == "in progress":
                availability = "assigned"
                assignee_id = self.id.get_assignee(
                    task_assignee, task=task,
                    rec_name=rec_name, func="get_rec_values")
                if assignee_id is None:
                    return None
                break
            elif task_status in ["defer", "barred"]:
                availability = task_status
                break

        # bundle all values of a recording and return them
        return 2*(rec_name, session_id, availability,
                  assignee_id, rec["quality"], rec["child speech"],
                  rec["directedness"], rec["Dene"], rec["audio"], rec["notes"])

    def get_progress_values(self, rec):
        """Get progress values for a recording."""
        # collect all progress records associated with a recording
        progress_values = []

        # go through each task type from monitor.csv
        for task in ["segmentation", "transcription/translation", "glossing"]:

            # get id of this task
            task_type_id = self.id.get_task_type(task)
            # get status of this task
            task_status = rec["status " + task]

            # 'defer' and 'barred' status become 'not started' in progress
            if task_status in ["barred", "defer"]:
                task_status = "not started"
            # get status for quality check
            if task == "segmentation":
                quality_check = "not required"
            else:
                quality_check = rec["status check " + task]

            progress_values.append(
                2*(rec["id"], task_type_id, task_status, quality_check, None))

        return progress_values

    def get_action_log_values(self, rec):
        """Get action log values for a recording."""
        # collect all action logs associated with a recording
        action_logs = []
        # get recording name and id
        rec_name = rec["recording name"]
        rec_id = rec["id"]

        # only actions 'assign', 'letcheck' and 'checkin' are relevant
        # for monitor, so get id of only those actions.
        assign_id = self.id.get_action("assign")
        checkin_id = self.id.get_action("checkin")
        letcheck_id = self.id.get_action("letcheck")

        # go through every task
        for task in ["segmentation", "transcription/translation", "glossing"]:

            # get task id and status
            task_type_id = self.id.get_task_type(task)
            task_status = rec["status " + task]

            # if task status is 'complete', 'incomplete' or 'in progress'
            # append an action log with the right action, time and assignee
            if task_status in ["complete", "incomplete", "in progress"]:

                # get id of task assignee
                task_assignee_id = self.id.get_assignee(
                    rec["person " + task], task=task,
                    rec_name=rec_name, func="get_action_log_values")
                if task_assignee_id is None:
                    return None

                # for the task status's 'complete' and 'incomplete'
                # the actions 'assign' and 'checkin' are triggered
                if task_status == "complete" or task_status == "incomplete":
                    action_logs.append(
                        2*(rec["start " + task], assign_id, rec_id, None,
                           task_type_id, None, task_assignee_id, None))
                    action_logs.append(
                        2*(rec["end " + task], checkin_id, rec_id, None,
                           task_type_id, None, task_assignee_id, None))
                # for task status 'in progress'
                # the action 'assign' is triggered
                elif task_status == "in progress":
                    action_logs.append(
                        2*(rec["start " + task], assign_id, rec_id, None,
                           task_type_id, None, task_assignee_id, None))

            # do the same for check fields
            # first check if task has a check field
            if task != "segmentation":

                # get check status
                check_status = rec["status check " + task]

                if check_status in ["complete", "incomplete", "in progress"]:

                    # get id of check assignee
                    check_assignee_id = self.id.get_assignee(
                        rec["person check " + task], task=task + "/check",
                        rec_name=rec_name, func="get_action_log_values")
                    if check_assignee_id is None:
                        return None

                    # for the check status's 'complete' and 'incomplete'
                    # the actions 'assign' and 'checkin' are triggered
                    if check_status in ["complete", "incomplete"]:
                        action_logs.append(
                            2*(rec["start check " + task], letcheck_id,
                               rec_id, None, task_type_id, None,
                               check_assignee_id, None))
                        action_logs.append(
                            2*(rec["end check " + task], checkin_id,
                               rec_id, None, task_type_id, None,
                               check_assignee_id, None))
                    # for check status 'in progress'
                    # the action 'letcheck' is triggered
                    elif check_status == "in progress":
                        action_logs.append(
                            2*(rec["start check " + task], letcheck_id,
                               rec_id, None, task_type_id, None,
                               check_assignee_id, None))

        return action_logs

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

            rec_id = self.id.get_rec(file["Recording code"],
                                     func="import_files")
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

            # TODO: ask rabart: distinction 'no' and 'no longer'?
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

    def wipe_all(self):
        """Delete all tables in the database."""
        # TODO: action log must not (!) be completely deleted
        # -> only actions that can be read from monitor:
        # assign, letcheck, checkin

        # delete all rows from all tables
        for table in ["action_log", "files", "sessions_and_participants",
                      "progress", "recordings", "sessions", "participants"]:

            self.wipe(table)

    def start(self):
        """Import from all files."""
        if self.args.radical:
            self.wipe_all()

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
        print()


def main():
    """Start database interface application."""
    DBInterface().run()


if __name__ == '__main__':
    main()
