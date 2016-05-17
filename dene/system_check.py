"""Extracts the metadata for resources and checks the resources on the server.

This modules includes two classes, one extracting metadata from resources and one checking the whole recording file system on
the server. If you run this module, make sure exiftool (http://www.sno.phy.queensu.ca/~phil/exiftool/) and
the python wrapper for it (https://smarnach.github.io/pyexiftool/) is installed.

If the script is run without any path specifications (via command line), the script will look for 'sessions.csv' and
'resources.csv' in the folder 'Metadata', for 'locations.csv' and 'monitor.csv' in the folder 'Workflow' and for the
resources itself in 'Media', all folders lying one level higher than the script itself. In this case the script will check
everything. You can also specify the paths to all those aforementioned files (see python3 system_check --help).
In this case, what checks are done effectively depends on which file paths were specified over the command line.
"""

import os
import re
import csv
import sys
import string
import argparse
import logging
import exiftool
from collections import defaultdict

# logging settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("resources.log", mode="w")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(funcName)s|%(levelname)s|%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

########################################################################################################################
########################################################################################################################

class Resource:
    """Class for extracting, checking and correcting the metadata of a resource."""


    # the four media file extensions are mapped to their MIME-Type and exiftool's key to access the duration
    media_dict = {
        "wav": ("Audio", "Composite"),
        "mp4": ("Video", "QuickTime"),
        "mts": ("Video", "M2TS"),
        "mov": ("Video", "QuickTime")
    }


    def __init__(self, path, exifTool):
        """Initialize and store path, name, extension and exiftool's instance of the media file.

        Positional args:
            path: path to the media file relative to the script's location
            et: an instance of exiftool for extracting the metadata of a media file
        """
        # store path to the media file relative to the script's location
        self.path = path
        # store name of the media file
        self.file_name = os.path.split(self.path)[1]
        # store (lowercased) extension of media file
        self.extension = self.file_name[-3:].lower()
        # store parsed media file by exiftool
        self.exifTool = exifTool.get_metadata(self.path)


    def get_Session_code(self):
        """Strip off extension part and any letters for partial sessions and return it"""
        match = re.search(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d+)?", self.file_name)

        if match:
            return match.group()
        else:
            return ""


    def get_Recording_code(self):
        """Strip off the dot and the file extension of the media file's name and return it."""
        return self.file_name[:-4]


    def get_Type(self):
        """Return the MIME-Type of the media file."""
        return Resource.media_dict[self.extension][0]


    def get_Format(self):
        """Return the MIME-Type of the media file followed by its extension."""
        return Resource.media_dict[self.extension][0] + "/" + self.extension


    def get_Duration(self):
        """Extract the duration (recording length) of a media file and return it in the format HH:MM:SS."""
        # try to extract the media file's duration in secs
        try:
            duration_in_secs = self.exifTool[Resource.media_dict[self.extension][1] + ":Duration"]
        except KeyError:
            logger.error("Duration cannot be extracted for " + self.file_name)
            return ""

        # convert to hours, minutes and seconds
        minutes, secs = divmod(duration_in_secs, 60)
        hours, minutes = divmod(minutes, 60)

        # output in the format HH:MM:SS
        return "%02d:%02d:%02d" % (hours, minutes, secs)


    def get_Byte_size(self):
        """Extract size of media file in bytes and return it."""
        # try to extract the media file's size in bytes
        try:
            bytes = self.exifTool["File:FileSize"]
        except KeyError:
            logger.error("Byte size cannot be extracted for " + self.file_name)
            return ""
        else:
            return bytes


    def get_Word_size(self):
        """Not yet implemented."""
        return ""


    def get_Location(self):
        """Return absolute path of media file."""
        return "smb://server.ivs.uzh.ch/Dene/Media/" + self.file_name


    def in_media_dict(self):
        """Check if the file has one of the following extensions: wav, mp4, mts, mov. Return True or False."""
        return self.extension in Resource.media_dict

########################################################################################################################
########################################################################################################################

class System_check:
    """Checks whole system on server."""


    def __init__(self):
        """Initializes various sets for the recording files."""
        # data structure for system: {session_code: {rec_code_A: {file.mp4, file.mts/mov, file.wav},...},...}
        self.media_structure = defaultdict(lambda: defaultdict(set))
        self.recs_from_media_folder = set()
        self.session_codes_from_sessions = set()
        self.recs_from_locations = set()
        self.rec_codes_from_locations = set()
        self.rec_codes_from_monitor = set()


    def set_media(self, media_path):
        """Get and set recording names from Media folder.

        Positional args:
            media_path: path to media folder
        """
        for rec in os.listdir(media_path):

            # get recording code
            rec_code = rec[:-4]

            # regex for checking and extracting parts of the recording code
            rec_code_regex = re.compile(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-([A-Z]+|\d+|\d+[A-Z]+))?")

            # check the format of recording code
            if rec_code_regex.fullmatch(rec_code):

                # infer the session code
                session_code = re.search(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d+)?", rec_code).group()

                # store recording name under the right session and recording code
                self.media_structure[session_code][rec_code].add(rec)

                # store recording name in a separate set
                self.recs_from_media_folder.add(rec)

            # if file is a hidden file, produce warning
            elif rec.startswith("."):
                logger.warning("File '" + rec + "' is a hidden file")

            else:
                logger.error("Format of " + rec + " wrong")


    def set_locations(self, locations_path):
        """Get and set recording names and recording codes from file_locations.csv.

        Positional args:
            locations_path: path to file_locations.csv
        """
        with open(locations_path, "r") as locations_file:
            for row in csv.DictReader(locations_file):
                if "yes" in row["UZH"]:
                    self.recs_from_locations.add(row["File name"])
                    self.rec_codes_from_locations.add(row["File name"][:-4])


    def set_monitor(self, monitor_path):
        """Get and set recording codes from monitor.csv.

        Positional args:
            monitor_path: path to monitor.csv
        """
        with open(monitor_path, "r") as monitor_file:
            self.rec_codes_from_monitor = {row["recording"] for row in csv.DictReader(monitor_file) if row["recording"]}


    def set_sessions(self, sessions_path):
        """Get and set session codes from sessions.csv.

        Positional args:
            sessions_path: path to sessions.csv
        """
        with open(sessions_path, "r") as sessions_file:
            self.session_codes_from_sessions = {row["Code"] for row in csv.DictReader(sessions_file)}


    def set_all(self, media_path, locations_path, monitor_path, sessions_path):
        """Gets and sets all data.

        Positional args:
            media_path: path to media folder
            locations_path: path to file_locations.csv
            monitor_path: path to monitor.csv
            sessions_path: path to sessions.csv
        """
        self.set_media(media_path)
        self.set_locations(locations_path)
        self.set_monitor(monitor_path)
        self.set_sessions(sessions_path)


    def autocomplete(self, resources_path, media_path):
        """Autocompletes resources.csv.

        Positional args:
            resources_path: path to resources.csv
            media_path: path to media folder
        """
        with open(resources_path, "r+") as resources_file, exiftool.ExifTool() as exifTool:
            # store recording names from resources.csv
            recs_from_resources = {row["File name"] for row in csv.DictReader(resources_file)}

            # create DictWriter instance for writing the metadata of new resources
            resources_writer = csv.DictWriter(resources_file, fieldnames=["Session code", "Recording code", "File name", "Type",
                "Format", "Duration", "Byte size", "Word size", "Location"])

            # system -> resources.csv
            new_recs = self.recs_from_media_folder - recs_from_resources

            # keep track of progress
            n_recs = len(new_recs)
            if n_recs:
                n_recs = str(len(new_recs))
                counter = 0
                print("Autocompletion for:")

            for rec in new_recs:

                # count and print progress
                counter += 1
                print(rec + "\t\t\t" + str(counter) + "/" + n_recs)

                # create an instance of the Resource class
                resource = Resource(media_path + "/" + rec, exifTool)

                # exclude any files that do not have the proper extension
                if resource.in_media_dict():

                    # write metadata to the file 'resources.csv'
                    resources_writer.writerow({
                        "Session code": resource.get_Session_code(),
                        "Recording code": resource.get_Recording_code(),
                        "File name": rec,
                        "Type": resource.get_Type(),
                        "Format": resource.get_Format(),
                        "Duration": resource.get_Duration(),
                        "Byte size": resource.get_Byte_size(),
                        "Word size": resource.get_Word_size(),
                        "Location": resource.get_Location()
                    })

                else:
                    logger.warning("File '" + rec + "' has unknown file extension")


    def media_check(self):
        """Checks consistency of recording files in the Media folder.

        The following checks are made:
            - consecutive letters in recording codes
            - consecutive numbers in session codes
            - every recording code occurs with a wav, mp4 and mts/mov extension
        """
        # hash storing same-day session codes (without numbers) mapped to a list with (ideally) consecutive numbers
        same_day_session_codes = defaultdict(list)

        # Go through all session codes
        for session_code in self.media_structure:

            # Check if session code has a number
            match = re.search(r"(.*\d\d\d\d\-\d\d\-\d\d)\-(\d+)$", session_code)
            if match:
                part_without_number = match.group(1)
                number = int(match.group(2))
                # save number with this session_code
                same_day_session_codes[part_without_number].append(number)

            # create list of (ideally) consecutive letters
            letter_seq_list = []

            # Go through all recording codes mapped to that session code
            for rec_code in self.media_structure[session_code]:

                # extract partial code letter
                match = re.search(r"[A-Z]+$", rec_code)
                if match:
                    letter_seq_list += list(match.group())

                self.three_files_check(rec_code, self.media_structure[session_code][rec_code])

            self.consecutive_letter_check(session_code, letter_seq_list)

        self.consecutive_number_check(same_day_session_codes)


    def three_files_check(self, rec_code, rec_set):
        """Checks if every recording code occurs with a wav, mp4 and mts/mov extension.

        positional args:
            rec_code: recording code under which the three files are subsumed
            rec_set: (ideally) contains three different file types
        """
        wav = rec_code + ".wav"
        mp4 = rec_code + ".mp4"
        mts = rec_code + ".mts"
        mov = rec_code + ".mov"

        # Check if file with wav-extension exists
        if wav not in rec_set:
            logger.warning(wav + " missing")

        # Check if file with mp4-extension exists
        if mp4 not in rec_set:
            logger.warning(mp4 + " missing")

        # Check if file with mov/mts-extension exists
        if mts not in rec_set and mov not in rec_set:
            logger.warning(mts + "/" + mov + " missing")


    def consecutive_letter_check(self, session_code, letter_seq_list):
        """Checks if letters are consecutive.

        Positional args:
            session_code: session code under which the recording codes are subsumed
            letter_seq_list: list containing letters of all recording codes under this session code
        """
        if letter_seq_list:

            # first sort letters
            letter_seq_list = sorted(letter_seq_list)

            # get 'largest' letter, i.e. letter closest to the end of the alphabet
            largest_letter = letter_seq_list[-1]

            # get position of that letter in the alphabet
            largest_letter_pos = string.ascii_uppercase.index(largest_letter)

            # extract the letters that should occur in the recording codes
            letters_that_should_occur = string.ascii_uppercase[:largest_letter_pos + 1]

            # check if recording code with 'A' exists, but not with 'B'
            if len(letter_seq_list) == 1 and "A" in letter_seq_list:
                logger.warning("Recording code " + session_code + "(-)B missing")

            # otherwise check if all required letters occur
            else:
                for letter in letters_that_should_occur:
                    if letter not in letter_seq_list:
                        logger.warning("Recording code " + session_code + "-" + letter + " missing")


    def consecutive_number_check(self, same_day_codes):
        """Check if same-day-session codes are consecutive.

        positional args:
            same_day_codes: hash mapping session code to a list of numbers
        """
        # go through all session codes without numbers
        for session_code_without_number in same_day_codes:

            # first sort all numbers
            numbers = sorted(same_day_codes[session_code_without_number])

            # extract the largest number
            largest_number = numbers[-1]

            # check if session code with '1' exists, but not with '2'
            if len(numbers) == 1 and 1 in numbers:
                logger.warning("Session code " + session_code_without_number + "-2 missing")

            # otherwise check if all required numbers occur
            else:
                for number in range(1, largest_number + 1):
                    if number not in numbers:
                        logger.warning("Session code " + session_code_without_number + "-" + str(number) + " missing")


    def compare_sessions_media(self):
        """Check if every session code in sessions.csv has at least one file in the media folder and vice versa."""
        # Check session.csv -> media folder
        for session_code in self.session_codes_from_sessions:
            if session_code not in self.media_structure:
                logger.warning(session_code + " from sessions.csv not in media folder")

        # Check media folder -> sessions.csv
        for session_code in self.media_structure:
            if session_code not in self.session_codes_from_sessions:
                logger.warning(session_code + " from media folder not in sessions.csv")


    def compare_locations_media(self):
        """Check if every recording name in file_locations.csv has a corresponding file in the media folder and vice versa."""
        # Check file_locations.csv -> media folder
        for rec in self.recs_from_locations - self.recs_from_media_folder:
            logger.warning(rec + " from file_locations.csv not in media folder")

        # Check media folder -> file_locations.csv
        for rec in self.recs_from_media_folder - self.recs_from_locations:
            logger.warning(rec + " from media folder not in file_locations.csv")


    def compare_locations_monitor(self):
        """Check if every recording code in file_locations.csv is also listed in monitor.csv and vice versa."""
        # Check file_locations.csv -> monitor.csv
        for rec in self.rec_codes_from_locations - self.rec_codes_from_monitor:
            logger.warning(rec + " from file_locations.csv not in monitor.csv")

        # Check monitor.csv -> file_locations.csv
        for rec in self.rec_codes_from_monitor - self.rec_codes_from_locations:
            logger.warning(rec + " from monitor.csv not in file_locations.csv or not at UZH yet")


    def check_all(self):
        """Checks whole system."""
        self.media_check()
        self.compare_sessions_media()
        self.compare_locations_media()
        self.compare_locations_monitor()


if __name__ == "__main__":

    # set up command line arguments
    arg_description =   """
                        Specify paths for media folder, sessions.csv, file_locations.csv, monitor.csv and resources.csv.
                        Keep in mind that one or more of the following file combinations must be given:
                        - media folder only
                        - media folder and resources.csv
                        - media folder and file_locations.csv
                        - media folder and sessions.csv
                        - locations.csv and monitor.csv
                        """

    parser = argparse.ArgumentParser(description=arg_description)
    parser.add_argument("-f", "--media", help="path to the media folder")
    parser.add_argument("-l", "--locations", help ="path to file_locations.csv")
    parser.add_argument("-m", "--monitor", help="path to monitor.csv")
    parser.add_argument("-r", "--resources", help="path ro resources.csv")
    parser.add_argument("-s", "--sessions", help="path to sessions.csv")
    args = parser.parse_args()

    # create instance for system check
    dene_recs = System_check()

    # default settings if no arguments were given via command line
    if len(sys.argv) == 1:

        # all default paths
        media_path = "../Media"
        locations_path = "../Workflow/file_locations.csv"
        monitor_path = "../Workflow/monitor.csv"
        sessions_path = "../Metadata/sessions.csv"
        resources_path = "../Metadata/resources.csv"

        # get all data from all files
        dene_recs.set_all(media_path, locations_path, monitor_path, sessions_path)
        # then check everything
        dene_recs.check_all()
        # finally complete resources.csv
        dene_recs.autocomplete(resources_path, media_path)

    elif args.media:
        # get and set recording files in the media folder
        dene_recs.set_media(args.media)
        # check the file names from the media folder
        dene_recs.media_check()

        if args.resources:
            # autocomplete resources.csv
            dene_recs.autocomplete(args.resources, args.media)

        if args.sessions:
            # get and set session codes from sessions.csv
            dene_recs.set_sessions(args.sessions)
            # check sessions.csv <-> media folder
            dene_recs.compare_sessions_media()

        if args.locations:
            # get and set recording names from locations.csv
            dene_recs.set_locations(args.locations)
            # check media folder <-> locations.csv
            dene_recs.compare_locations_media()

            if args.monitor:
                # get and set recording codes from monitor.csv
                dene_recs.set_monitor(args.monitor)
                # check locations.csv <-> monitor.csv
                dene_recs.compare_locations_monitor()

    else:

        if args.locations and args.monitor:
            # get and set recording codes from locations.csv
            dene_recs.set_locations(args.locations)
            # get and set recording codes from monitor.csv
            dene_recs.set_monitor(args.monitor)
            # check locations.csv <-> monitor.csv
            dene_recs.compare_locations_monitor()

        else:
            print("You have not given the right combination of files via command line. Try again.")



    # close logging file
    handler.close()
