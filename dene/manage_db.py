import MySQLdb as db
import csv
import argparse
import traceback
import sys


def commandline_setup():
    """Set up command line arguments"""
    arg_description = """Specify paths for sessions.csv, participants.csv and resources.csv"""
    parser = argparse.ArgumentParser(description=arg_description)

    ####### files
    parser.add_argument("--metadata", action="store_true")
    parser.add_argument("--sessions", help="path to sessions.csv", default="../Metadata/sessions.csv")
    parser.add_argument("--participants", help="path to participants.csv", default="../Metadata/participants.csv")
    parser.add_argument("--files", help="path to files.csv", default="../Metadata/files.csv")
    parser.add_argument("--monitor", help="path to monitor.csv", default="../Workflow/monitor.csv")
    ####### task options

    return parser.parse_args()


class DB_Manager:

    def __init__(self, con):

        self.con = con
        self.cur = self.con.cursor()
        self.args = commandline_setup()


    def wipe(self, table):
        """Delete all rows of a table"""
        self.cur.execute("""DELETE FROM {};""".format(table))
        self.con.commit()


    def empty_str_to_none(self, row):
        "Set all empty strings to None"
        for field in row:
            if not row[field]:
                row[field] = None


    def insert(self, table, db_attributes, values, len):
        """Insert values into a table"""

        sql_command = "INSERT INTO " + table + db_attributes + " VALUES (" + ",".join(["%s"]*len) + ")"

        try:
            self.cur.execute(sql_command, values)

        except db.Error:
            print("\n")
            traceback.print_exc(limit=0)
            print("Check the following row in {}:".format(table), values)

        self.con.commit()


    def fill_sessions(self):
        """Refreshes table 'sessions' completely by filling it with data from sessions.csv"""
        db_attributes = "(name, date, location, duration, situation, content, notes)"

        self.wipe("sessions")

        # try reading sessions.csv
        try:
            sessions_file = open(self.args.sessions, "r")
        except FileNotFoundError:
            print("Path to sessions.csv not correct!")
            sys.exit(1)

        # go through each session
        for p in csv.DictReader(sessions_file):

            self.empty_str_to_none(p)

            values = (p["Code"], p["Date"], p["Location"], p["Length of recording"], p["Situation"], p["Content"], p["Comments"])

            self.insert("sessions", db_attributes, values, 7)


    def fill_participants(self):
        """Refresh table 'participants' completely by filling it with data from participants.csv"""
        # issues:
        #   - change email field not working
        #   - what about phone?
        #   - main language -> only one value allowed? -> adaption in metadata.py? / remove n/a

        db_attributes = """(
            short_name, first_name, last_name, birthdate, age, gender, education, first_languages,
            second_languages, main_language, language_biography, description, contact_address, email
        )"""

        self.wipe("participants")

        # try reading participants.csv
        try:
            participants_file = open(self.args.participants, "r")
        except FileNotFoundError:
            print("Path to participants.csv not correct!")
            sys.exit(1)

        # go through each participant
        for p in csv.DictReader(participants_file):

            self.empty_str_to_none(p)

            # extract first-/lastname assuming only the first can consist of more than one word (not foolproof...)
            *first_name, last_name = p["Full name"].split()

            # create sets for language fields that have more than one value
            for field in ["Main language", "First languages", "Second languages"]:
                if p[field] is not None:
                    p[field] = set(p[field].split("/"))

            values = (
                p["Short name"], " ".join(first_name), last_name, p["Birth date"], p["Age"], p["Gender"], p["Education"],
                p["First languages"], p["Second languages"], p["Main language"], p["Language biography"], p["Description"],
                p["Contact address"], p["E-mail/Phone"]
            )

            self.insert("participants", db_attributes, values, 14)


    def fill_database(self):
        self.fill_participants()
        self.fill_sessions()


    def test(self):
        """Just for testing"""
        self.cur.execute("""INSERT INTO participants (short_name, first_name, last_name) VALUES (%s, %s, %s)""", ("CDF", "töst", "Töst"))
        self.con.commit()
        self.cur.execute("""SELECT * FROM participants;""")
        print(self.cur.fetchone())


def main():

    con = db.connect(host="localhost", user="anna", passwd="anna", db="deslas", charset="utf8")

    populator = DB_Manager(con)
    populator.fill_sessions()

    con.close()


if __name__ == '__main__':
    main()
