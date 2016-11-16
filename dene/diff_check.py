"""This module checks if the module manage_db.py works properly.

It imports and exports the metadata of Dene twice and compares the content of
the databases and csv files. If the contents are not identical, a file will be
created where the lines that differ are highlighted.

Output format can be a txt or html file (default: txt) and can be set by the
argument --format. This test module has to lie in the same directory as the
module manage_db.py. The module will create a directory called
'Unittest-diffcheck_<date>' where the files of both exports, the database logs
of the import and all diffs are contained.

Example test:
    python3 diff_check.py [--format txt|html]
"""


import os
import sys
import time
import shutil
import difflib
import argparse
import manage_db
from tqdm import tqdm
import MySQLdb as db


class TestDbInterface:

    # The id of certain record can change for every import.
    # To compare two sql tables all foreign keys must be resolved first, i.e.
    # every foreign key is replaced by attributes that can be alternate keys.
    # The following hash stores the attributes names forming an alternate key
    # and the join command for getting the attributes values.
    JOIN_DATA = {
        "action_log":
            (["action", "recordings.name", "files.name", "task_types.name",
              "e1.short_name", "e2.short_name"],
             """JOIN actions ON action_log.action_fk=actions.id
                JOIN recordings ON action_log.recording_fk=recordings.id
                LEFT JOIN files ON action_log.file_fk=files.id
                JOIN task_types ON action_log.task_type_fk=task_types.id
                LEFT JOIN employees e1 ON action_log.client_fk=e1.id
                LEFT JOIN employees e2 ON action_log.assignee_fk=e2.id"""),
        "files":
            (["recordings.name"],
             "JOIN recordings ON files.recording_fk=recordings.id"),
        "progress":
            (["recordings.name", "task_types.name"],
             """JOIN recordings ON progress.recording_fk=recordings.id
                JOIN task_types ON progress.task_type_fk=task_types.id"""),
        "recordings":
            (["sessions.name"],
             "JOIN sessions ON session_fk=sessions.id"),
        "sessions_and_participants":
            (["name", "short_name"],
             """JOIN sessions
                ON sessions_and_participants.session_fk=sessions.id
                JOIN participants
                ON sessions_and_participants.participant_fk=participants.id
             """),
        "versions":
            (["files.name", "time", "recordings.name"],
             """JOIN files ON versions.file_fk=files.id
                JOIN action_logs ON versions.trigger_fk=action_logs.id
                JOIN recordings ON action_logs.recording_fk=recordings.id"""),
        "participants": ([], ""),
        "sessions": ([], "")
    }

    # directory path where outputs from testing the db interface are collected
    OUTPUT_PATH = "Unittest-diffcheck_" + time.strftime("%d-%m-%Y")
    # path to Export directory that is created when exporting
    EXPORT_PATH = os.path.join(OUTPUT_PATH, "Export/")

    def __init__(self):
        """Get cmdline arguments and create output directory. """
        # get command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("--format", choices=["html", "txt"])
        self.args = parser.parse_args()

        # if this directory path already exists, remove it
        if os.path.exists(self.OUTPUT_PATH):
            shutil.rmtree(self.OUTPUT_PATH)

        # create directory collecting outputs from running the database
        os.mkdir(self.OUTPUT_PATH)

        # default command line arguments for import and export
        self.import_args = ["import"]
        self.export_args = ["export", "--path", self.OUTPUT_PATH]

    def get_import_args(self, dir_path):
        """Get list of command line arguments for database import"""

        args = ["import"]

        for name, filepath in [("-s", "sessions.csv"),
                               ("-p", "participants.csv"),
                               ("-m", "monitor.csv"),
                               ("-l", "file_locations.csv"),
                               ("-f", "files.csv")]:

            args.append(name)
            args.append(os.path.join(dir_path, filepath))

        args.append("-r")

        return args

    def get_csv_content(self):
        """Get content of all metadata files as strings."""
        content = {}
        for filename in os.listdir(self.EXPORT_PATH):
            filepath = os.path.join(self.EXPORT_PATH, filename)

            with open(filepath, "r") as f:
                content[filename] = sorted(f.readlines())
                f.flush()

        return content

    def get_db_content(self):
        """Get content of all database tables as strings."""
        content = {}

        con = db.connect(host="localhost", user="anna", passwd="anna",
                         db="deslas", charset="utf8")

        cur = con.cursor()

        db_attrs = manage_db.Import.db_attrs

        for table in db_attrs:

            # get and stringify to be selected attributes ignoring foreign keys
            selected_attrs = ",".join(
                [table + "." + attr for attr in db_attrs[table]
                 if not attr.endswith("_fk")]
                + self.JOIN_DATA[table][0])

            # fetch data from table
            cur.execute("SELECT {} FROM {} {}".format(
                selected_attrs, table, self.JOIN_DATA[table][1]))

            # stringify and save data as sorted list of lines
            content[table] = sorted([",".join(str(field) for field in record)
                                    for record in cur])

        cur.close()
        con.close()

        return content

    def run_db_interface(self, args):
        """Run database interface.

        args (list): set command line arguments
        """
        sys.argv[1:] = args
        manage_db.main()

    def compare(self, content1, content2):
        """Compare contents of databases or csv files.

        content1/content2:
            dictionaries containing list of stringifed data for each
            csv-file/db-table. Both contents must contain the same keys.
        """
        for key in tqdm(content1):

            lines1 = content1[key]
            lines2 = content2[key]

            if lines1 == lines2:
                print(key, "identical!")
                sys.stdout.flush()
            else:
                print(key, "not identical! Diff will be created...", end="")
                sys.stdout.flush()

                # create directory for all diffs if does not already exist
                path = os.path.join(self.OUTPUT_PATH, "diffs")
                if not os.path.isdir(path):
                    os.mkdir(path)

                if self.args.format == "html":

                    with open(os.path.join(path, key + ".html"), "w") as f:

                        f.write(difflib.HtmlDiff().make_file(
                            lines1, lines2, fromdesc=key + "1",
                            todesc=key + "2"))
                else:
                    with open(os.path.join(path, key + ".diff"), "w") as f:
                        for line in difflib.unified_diff(
                                lines1, lines2, fromfile=key + "1",
                                tofile=key + "2"):

                            f.write(line)
                            f.write("\n")

                print("done.")
                sys.stdout.flush()

    def check(self):
        """Do the checks."""
        print("**********First Import**********")
        sys.stdout.flush()
        self.run_db_interface(self.import_args)
        db_content1 = self.get_db_content()
        os.rename("db.log", "db1.log")
        shutil.move("db1.log", self.OUTPUT_PATH)

        print("**********First Export**********")
        sys.stdout.flush()
        self.run_db_interface(self.export_args)
        csv_content1 = self.get_csv_content()
        export1_path = os.path.join(self.OUTPUT_PATH, "Export1/")
        os.rename(self.EXPORT_PATH, export1_path)

        print("**********Second Import**********")
        sys.stdout.flush()
        self.import_args = self.get_import_args(export1_path)
        self.run_db_interface(self.import_args)
        db_content2 = self.get_db_content()
        os.rename("db.log", "db2.log")
        shutil.move("db2.log", self.OUTPUT_PATH)

        print("**********Second Export**********")
        sys.stdout.flush()
        self.run_db_interface(self.export_args)
        csv_content2 = self.get_csv_content()
        export2_path = os.path.join(self.OUTPUT_PATH, "Export2/")
        os.rename(self.EXPORT_PATH, export2_path)

        print("**********Comparison of csv files**********")
        sys.stdout.flush()
        self.compare(csv_content1, csv_content2)

        print()

        print("**********Comparison of database tables**********")
        sys.stdout.flush()
        self.compare(db_content1, db_content2)


def main():
    """Start test."""
    test = TestDbInterface()
    # set path to original metadata files
    # test.import_args = test.get_import_args("shared/metadata/")
    test.check()

if __name__ == '__main__':
    main()
