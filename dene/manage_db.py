import MySQLdb as db
import _mysql_exceptions
import csv
import argparse


def commandline_setup():
    """Set up command line arguments"""
    arg_description = """Specify paths for sessions.csv, participants.csv and resources.csv"""
    parser = argparse.ArgumentParser(description=arg_description)

    ####### files
    parser.add_argument("-s", "--sessions", help="path to sessions.csv")
    parser.add_argument("-p", "--participants", help="path to participants.csv")
    parser.add_argument("-f", "--files", help="path to files.csv")
    parser.add_argument("-m", "--monitor", help="path to monitor.csv")
    ####### task options


    return parser.parse_args()


class DB_Manager:

    def __init__(self, con):

        self.con = con
        self.cur = self.con.cursor()

        self.args = commandline_setup()


    def fill_participants(self):
        """Refreshes table 'participants' completely by filling it with data from participants.csv """
        # wipe table 'participants' first
        self.cur.execute("""DELETE FROM participants;""")
        self.con.commit()

        # default path for participants.csv
        participants_path = "../Metadata/participants.csv"
        # overwrite path if given over command line
        if self.args.participants:
            participants_path = self.args.participants

        # open participants.csv for reading
        with open(participants_path, "r") as participants_file:

            # go through each participant
            for p in csv.DictReader(participants_file):

                # empty strings should become null values
                for field in p:
                    if not p[field]:
                        p[field] = None

                # extract first-/lastname assuming only the first can consist of more than one word (not foolproof...)
                *first_name, last_name = p["Full name"].split()

                # create sets for language fields that have more than one value
                for field in ["Main language", "First languages", "Second languages"]:
                    if p[field] is not None:
                        p[field] = set(p[field].split("/"))


                # issues:
                #   - change email field not working
                #   - what about phone?

                try:
                    self.cur.execute("""INSERT INTO participants (
                                            short_name, first_name, last_name, birthdate, age, gender,
                                            education, first_languages, second_languages, main_language,
                                            language_biography, description, contact_address, email
                                            )

                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                                            p["Short name"], " ".join(first_name), last_name,
                                            p["Birth date"], p["Age"], p["Gender"], p["Education"],
                                            p["First languages"], p["Second languages"], p["Main language"],
                                            p["Language biography"], p["Description"], p["Contact address"], p["E-mail/Phone"]
                                        )

                    )

                # except _mysql_exceptions.IntegrityError:
                #     continue
                # temporary workaround
                except UnicodeEncodeError:
                    continue

                self.con.commit()


    def fill_database(self):
        self.fill_participants()

    def test(self):
        """Just for testing"""
        self.cur.execute("""INSERT INTO participants (short_name, first_name, last_name) VALUES (%s, %s, %s)""", ("CDF", "töst", "Töst"))
        self.con.commit()
        self.cur.execute("""SELECT * FROM participants;""")
        print(self.cur.fetchone())

def main():

    con = db.connect(host="localhost", user="anna", passwd="anna", db="deslas")

    populator = DB_Manager(con)
    populator.fill_participants()

    con.close()


if __name__ == '__main__':
    main()
