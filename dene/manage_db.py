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


    def wipe(self, table, associated_tables=()):
        """Delete all rows of a table"""
        # disable foreign key checks in all tables associated with this table
        for associated_table in associated_tables:
            self.cur.execute("""ALTER TABLE {} NOCHECK CONSTRAINT all""".format(associated_table))
            self.con.commit()

        # delete all rows
        self.cur.execute("""DELETE FROM {};""".format(table))
        self.con.commit()

        # enable foreign key checks again in all tables associated with this table
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


    def execute(self, command, values):
        """Execute SQL commands and catch any SQL errors"""

        try:
            self.cur.execute(command, values)
        except db.OperationalError:
#            print("\n")
#            print("******************************")
#            traceback.print_exc(limit=0)
#            print("Check the following row:", values)
            pass
        except db.DataError:
#            print("\n")
#            print("******************************")
#            traceback.print_exc(limit=0)
#            print("Check the following row:", values)
            pass

        self.con.commit()


    def get_insert_command(self, table, db_attributes):
        """Create INSERT command with given attributes and return it"""

        insert_command = "INSERT INTO {} ({}) VALUES ({})".format(
            table,
            ",".join(db_attributes),
            ",".join(["%s"]*len(db_attributes))
        )

        return insert_command


    def get_update_command(self, table, db_attributes):
        """Create UPDATE command with given attributes and return it"""

        update_command = "UPDATE {} SET {} WHERE id = {{}}".format(
            table,
            ','.join((attr + "=%s") for attr in db_attributes),
        )

        return update_command


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
        """Refreshe table 'sessions' completely by filling it with data from sessions.csv"""

        db_attributes = ("name", "date", "location", "duration", "situation", "content", "notes")

        command = self.get_insert_update_command("sessions", db_attributes)

        # try reading sessions.csv
        try:
            sessions_file = open(self.args.sessions, "r")
        except FileNotFoundError:
            print("Path to sessions.csv not correct!")
            sys.exit(1)

        # go through each session
        for p in csv.DictReader(sessions_file):

            self.empty_str_to_none(p)

            values = (
                p["Code"], p["Date"], p["Location"], p["Length of recording"],
                p["Situation"], p["Content"], p["Comments"]
            )

            # insert/update session
            self.execute(command, values + values)

            # get session id in database
            self.cur.execute("""SELECT LAST_INSERT_ID()""")
            session_id = self.cur.fetchone()[0]

            # link session to participants
            self.refresh_sessions_participants(p["Participants and roles"], session_id)


    # TODO: uzh:phpmyadmin -> change in sessions_and_participants, 'role' enum to -> set
    def refresh_sessions_participants(self, participants_roles, session_id):
        """Refresh the table sessions_and_participants"""

        db_attributes = ("session_fk", "participant_fk", "role")

        if participants_roles:

            # go through participants and their roles
            for part_roles in participants_roles.split("), "):

                # try to extract shortname and its roles
                try:
                    shortname, roles = part_roles.split(" (")
                except ValueError:
                    # TODO: log
                    continue

                # create set of roles
                role_set = set(roles.split(" & "))

                # get id of this participant with this short name
                # TODO: create index on short_name to make it faster?
                self.cur.execute("""SELECT id FROM participants WHERE short_name = '{}'""".format(shortname))

                participant_id = self.cur.fetchone()

                if participant_id is None:
                    # TODO: log
                    continue

                command = self.get_insert_update_command("sessions_and_participants", db_attributes, has_id=False)

                values = (session_id, participant_id[0], role_set)

                self.execute(command, values + values)


    def import_participants(self):
        """Refresh table 'participants' completely by filling it with data from participants.csv"""

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
        for p in csv.DictReader(participants_file):

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

            self.execute(command, values + values)


    def refresh_database(self):
        #self.wipe("sessions")
        #self.wipe("participants")
        self.import_participants()
        self.import_sessions()
        #self.refresh_sessions_participants()


    def test(self):
        """Just for testing"""
        self.cur.execute("""INSERT INTO participants (short_name, first_name, last_name) VALUES (%s, %s, %s)""", ("CDF", "töst", "Töst"))
        self.con.commit()
        self.cur.execute("""SELECT * FROM participants;""")
        print(self.cur.fetchone())



def main():

    con = db.connect(host="localhost", user="anna", passwd="anna", db="deslas", charset="utf8")

    populator = DB_Manager(con)
    populator.refresh_database()
    print("done")
    con.close()


if __name__ == '__main__':
    main()
