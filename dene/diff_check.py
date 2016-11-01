"""This module checks if the module manage_db.py works properly.

It imports and exports twice and compares the content of the databases and
csv files. If the contents are not identical, an file will be created
where the lines that differ are shown. Output format can be a txt or html file.
"""

import difflib
import argparse
import os
import sys
import manage_db
from tqdm import tqdm
import MySQLdb as db

# TODO: class structure

parser = argparse.ArgumentParser()
parser.add_argument("--format", choices=["html", "txt"])
args = parser.parse_args()

# tables with (fk attributes, join command)-tuples for resolving foreign keys
joins = {
    "action_log":
        (["action", "recordings.name", "files.name", "task_types.name",
          "e1.short_name", "e2.short_name"],
         """JOIN actions ON action_log.action_fk=actions.id
            JOIN recordings ON action_log.recording_fk=recordings.id
            JOIN files ON action_log.file_fk=files.id
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
            ON sessions_and_participants.participant_fk=participants.id"""),
    "versions":
        (["files.name", "time", "recordings.name"],
         """JOIN files ON versions.file_fk=files.id
            JOIN action_logs ON versions.trigger_fk=action_logs.id
            JOIN recordings ON action_logs.recording_fk=recordings.id"""),
    "participants": ([], ""),
    "sessions": ([], "")
}


def get_import_args(dir_path):
    """Get list of split cmdline arguments for database import"""

    split_args = ["import"]

    for name, filepath in [("-s", "sessions.csv"),
                           ("-p", "participants.csv"),
                           ("-m", "monitor.csv"),
                           ("-l", "file_locations.csv"),
                           ("-f", "files.csv")]:

        split_args.append(name)
        split_args.append(os.path.join(dir_path, filepath))

    split_args.append("-r")

    return split_args


def get_csv_content(path):
    """Get content of all metadata files as strings."""
    content = {}
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)

        with open(filepath, "r") as f:
            content[filename] = f.readlines()

    return content


def get_db_content():
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
            + joins[table][0])

        # fetch data from table
        cur.execute("SELECT {} FROM {} {}".format(selected_attrs,
                                                  table,
                                                  joins[table][1]))

        # stringify and save data as list of lines
        content[table] = [",".join(str(field) for field in record)
                          for record in cur]

    cur.close()
    con.close()

    return content


def run(args):
    """Set command line arguments and run database interface application."""
    sys.argv[1:] = args
    manage_db.main()


def compare(content1, content2):
    global args
    """Compare contents of databases or csv files.

    content1/content2:
        dictionaries containing list of stringifed data
        for each csv-file/db-table. Both contents must contain the same keys.
    """

    diff = difflib.HtmlDiff()

    for key in tqdm(content1):

        lines1 = content1[key]
        lines2 = content2[key]

        if lines1 == lines2:
            print(key, "identical!")
            sys.stdout.flush()
        else:
            print(key, "not identical! Diff will be created...", end="")
            sys.stdout.flush()

            # path for all diffs
            path = "./diffs"

            # create 'diffs' directory if it not already exists
            if not os.path.isdir(path):
                os.mkdir(path)

            if args.format == "html":

                with open(os.path.join(path, key + ".html"), "w") as f:

                    f.write(diff.make_file(lines1, lines2,
                                           fromdesc=key + "1",
                                           todesc=key + "2"))
            else:
                with open(os.path.join(path, key + ".diff"), "w") as f:
                    for line in difflib.unified_diff(lines1, lines2,
                                                     fromfile=key + "1",
                                                     tofile=key + "2"):

                        f.write(line)
                        f.write("\n")

            print("done.")
            sys.stdout.flush()


# default command line arguments for import and export
import_args = ["import"]
export_args = ["export"]

print("**********First Import**********")
sys.stdout.flush()
run(get_import_args("shared/metadata/"))
db_content1 = get_db_content()

print("**********First Export**********")
sys.stdout.flush()
run(export_args)
csv_content1 = get_csv_content("Export/")

print("**********Second Import**********")
sys.stdout.flush()
run(get_import_args("Export/"))
db_content2 = get_db_content()

print("**********Second Export**********")
sys.stdout.flush()
run(export_args)
csv_content2 = get_csv_content("Export/")

print("**********Comparison of csv files**********")
sys.stdout.flush()
compare(csv_content1, csv_content2)

print()

print("**********Comparison of database tables**********")
sys.stdout.flush()
compare(db_content1, db_content2)
