"""This module checks various sets representing sessions, recordings, and file names in the Dene corpus
for mutual consistency and automatically creates file-related metadata.

Requirements:
exiftool (http://www.sno.phy.queensu.ca/~phil/exiftool/)
pyexiftool (https://smarnach.github.io/pyexiftool/)

Input (default locations; execute python3 system_check.py --help for help on how to set different locations):
../Media
../Workflow/file_locations.csv
../Workflow/monitor.csv
../Metadata/sessions.csv
../Metadata/files.csv

Output:
../Metadata/files.csv
./filess.log
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

handler = logging.FileHandler("files.log", mode="w")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(funcName)s|%(levelname)s|%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

########################################################################################################################
########################################################################################################################

class File:
    """Class for extracting, checking and correcting the metadata of a file."""

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
        return File.media_dict[self.extension][0]


    def get_Format(self):
        """Return the MIME-Type of the media file followed by its extension."""
        return File.media_dict[self.extension][0] + "/" + self.extension


    def get_Duration(self):
        """Extract the duration (recording length) of a media file and return it in the format HH:MM:SS."""
        # try to extract the media file's duration in secs
        try:
            duration_in_secs = self.exifTool[File.media_dict[self.extension][1] + ":Duration"]
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
        return self.extension in File.media_dict

########################################################################################################################
########################################################################################################################

class System:
    """Checks whole system on server."""

    def __init__(self):
        """Initialize various sets for the file names."""
        # data structure for system: {session_code: {rec_code_A: {file.mp4, file.mts/mov, file.wav},...},...}
        self.media_structure = defaultdict(lambda: defaultdict(set))
        self.file_names_from_media_folders = set()
        self.session_codes_from_sessions = set()
        self.file_names_from_locations = set()
        self.rec_codes_from_locations = set()
        self.rec_codes_from_monitor = set()


    def set_media(self, folder_path_list):
        """Get and set file names from Media folders.

        Positional args:
            folder_path_list: list containing paths to folders containing media(-related) files
        """
        # go through media folders
        for path in folder_path_list:
            # walk folders recursively
            for root, folders, files in os.walk(path):
                # go through all file names
                for file_name in files:
                    # get recording code
                    rec_code = file_name[:-4]

                    # Check format of recording code
                    if self.has_correct_format(file_name):

                        # infer the session code
                        session_code = re.search(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d+)?", rec_code).group()

                        # store file name under the right session and recording code
                        self.media_structure[session_code][rec_code].add(file_name)

                        # store file name in a separate set
                        self.file_names_from_media_folders.add(file_name)


    def set_locations(self, locations_path):
        """Get and set file names and recording codes from file_locations.csv.

        Positional args:
            locations_path: path to file_locations.csv
        """
        with open(locations_path, "r") as locations_file:
            for row in csv.DictReader(locations_file):
                if "yes" in row["UZH"] or "sync" in row["UZH"]:
                    self.file_names_from_locations.add(row["File name"])
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


    def set_all(self, folder_path_list, locations_path, monitor_path, sessions_path):
        """Gets and sets all data.

        Positional args:
            folder_path_list: list containing paths to folders containing media(-related) files
            locations_path: path to file_locations.csv
            monitor_path: path to monitor.csv
            sessions_path: path to sessions.csv
        """
        self.set_media(folder_path_list)
        self.set_locations(locations_path)
        self.set_monitor(monitor_path)
        self.set_sessions(sessions_path)


    def autocomplete(self, files_path, folder_path_list):
        """Autocompletes files.csv.

        Positional args:
            files_path: path to files.csv
            folder_path_list: list containing paths to folders containing media(-related) files
        """
        with open(files_path, "r+") as files_file, exiftool.ExifTool() as exifTool:
            # store file names from files.csv
            file_names_from_files = {row["File name"] for row in csv.DictReader(files_file)}
            # create DictWriter instance for writing the metadata of those new files
            files_writer = csv.DictWriter(files_file, fieldnames=["Session code", "Recording code", "File name", "Type",
            "Format", "Duration", "Byte size", "Word size", "Location"])

            # go through media folders
            for path in folder_path_list:
                # walk folders recursively
                for root, folders, files in os.walk(path):
                    # get file names not yet in files.csv and exclude those having a wrong format
                    new_files = [file_name for file_name in files
                        if file_name not in file_names_from_files and self.has_correct_format(file_name)]

                    # if there a new files
                    if new_files:

                        print("Autocompletion for files in " + root)
                        n_files = str(len(new_files))

                        #  go through those files
                        for index, new_file in enumerate(new_files, 1):

                            # create an instance of the File class
                            file = File(root + "/" + new_file, exifTool)

                            # exclude any files that do not have the proper extension
                            if file.in_media_dict():

                                print(new_file + "\t\t\t" + str(index) + "/" + n_files)

                                # write metadata to the file 'files.csv'
                                files_writer.writerow({
                                    "Session code": file.get_Session_code(),
                                    "Recording code": file.get_Recording_code(),
                                    "File name": new_file,
                                    "Type": file.get_Type(),
                                    "Format": file.get_Format(),
                                    "Duration": file.get_Duration(),
                                    "Byte size": file.get_Byte_size(),
                                    "Word size": file.get_Word_size(),
                                    "Location": file.get_Location()
                                })

                            else:
                                logger.warning("File '" + new_file + "' has unknown file extension")

                    else:
                        print("No autocompletion from " + root)


    def media_check(self):
        """Checks consistency of file names in the media folders.

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

                # the letter coding the partial session
                match = re.search(r"[A-Z]+$", rec_code)
                if match:
                    letter_seq_list += list(match.group())

                self.three_files_check(rec_code, self.media_structure[session_code][rec_code])

            self.consecutive_letter_check(session_code, letter_seq_list)

        self.consecutive_number_check(same_day_session_codes)


    def three_files_check(self, rec_code, file_name_set):
        """Checks if every recording code occurs with a wav, mp4 and mts/mov extension.

        positional args:
            rec_code: recording code under which the three files are subsumed
            file_name_set: (ideally) contains three different file types
        """

        # Check if files with those extension exist
        for file_extension in [".wav", ".mp4"]:
            file_name = rec_code + file_extension
            if file_name not in file_name_set:
                logger.warning(file_name + " not in media folders")

        # Check if file with mov or mts extension exists
        if rec_code + ".mts" not in file_name_set and rec_code + ".mov" not in file_name_set:
            logger.warning(rec_code + ".mts/.mov" + " not in media folders")


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
                logger.warning("Recording code " + session_code + "(-)B not in media folders")

            # otherwise check if all required letters occur
            else:
                for letter in letters_that_should_occur:
                    if letter not in letter_seq_list:
                        logger.warning("Recording code " + session_code + "-" + letter + " not in media folders")


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
                logger.warning("Session code " + session_code_without_number + "-2 not in media folders")

            # otherwise check if all required numbers occur
            else:
                for number in range(1, largest_number + 1):
                    if number not in numbers:
                        logger.warning("Session code " + session_code_without_number + "-" + str(number) + " not in media folders")


    def compare_sessions_media(self):
        """Check if every session code in sessions.csv has at least one file in the media folders and vice versa."""
        # Check sessions.csv -> media folders
        for session_code in self.session_codes_from_sessions:
            if session_code not in self.media_structure:
                logger.warning(session_code + " from sessions.csv not in media folders")

        # Check media folders -> sessions.csv
        for session_code in self.media_structure:
            if session_code not in self.session_codes_from_sessions:
                logger.warning(session_code + " from media folders not in sessions.csv")


    def compare_locations_media(self):
        """Check if every file name in file_locations.csv has a corresponding file in the media folders and vice versa."""
        # Check file_locations.csv -> media folders
        for file_name in self.file_names_from_locations - self.file_names_from_media_folders:
            logger.warning(file_name + " from file_locations.csv not in media folders")

        # Check media folders -> file_locations.csv
        for file_name in self.file_names_from_media_folders - self.file_names_from_locations:
            logger.warning(file_name + " from media folders not in file_locations.csv")


    def compare_locations_monitor(self):
        """Check if every recording code in file_locations.csv is also listed in monitor.csv and vice versa."""
        # Check file_locations.csv -> monitor.csv
        for rec_code in self.rec_codes_from_locations - self.rec_codes_from_monitor:
            logger.warning(rec_code + " from file_locations.csv not in monitor.csv")

        # Check monitor.csv -> file_locations.csv
        for rec_code in self.rec_codes_from_monitor - self.rec_codes_from_locations:
            logger.warning(rec_code + " from monitor.csv not in file_locations.csv or not at UZH yet")


    def check_all(self):
        """Checks whole system."""
        self.media_check()
        self.compare_sessions_media()
        self.compare_locations_media()
        self.compare_locations_monitor()


    def has_correct_format(self, file_name):
        """Check if the recording code is in the right format"""
        # strip extension part
        rec_code = file_name[:-4]
        # regex for checking recording code
        rec_code_regex = re.compile(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d*[A-Z]*)?")
        # check format of recording code
        if rec_code_regex.fullmatch(rec_code):
            return True
        # if file is a hidden file, produce warning (except for '.DS_Store')
        elif file_name.startswith("."):
            if file_name != ".DS_Store":
                logger.warning("File '" + rec_code + "' is a hidden file")
            return False
        else:
            logger.error("Format of recording code '" + rec_code + "' not correct")
            return False

########################################################################################################################
########################################################################################################################

if __name__ == "__main__":

    # set up command line arguments
    arg_description =   """
                        Specify paths for media folders, sessions.csv, file_locations.csv, monitor.csv and files.csv.
                        Keep in mind that only some of the file combinations are valid:
                        - system_check.py
                        - system_check.py -f (-r)? (-s)? (-l (-m)?)?
                        - system_check.py -l -m
                        """

    parser = argparse.ArgumentParser(description=arg_description)
    parser.add_argument("-f", "--media", help="paths to folders containing media(-related files)", nargs="+")
    parser.add_argument("-l", "--locations", help ="path to file_locations.csv")
    parser.add_argument("-m", "--monitor", help="path to monitor.csv")
    parser.add_argument("-r", "--files", help="path ro files.csv")
    parser.add_argument("-s", "--sessions", help="path to sessions.csv")
    args = parser.parse_args()

    # create instance for system check
    dene_files = System()

    # default settings if no arguments were given via command line
    if len(sys.argv) == 1:

        # all default paths
        media_path = "../Media"
        rsync_path = "../rsync-folder"
        locations_path = "../Workflow/file_locations.csv"
        monitor_path = "../Workflow/monitor.csv"
        sessions_path = "../Metadata/sessions.csv"
        files_path = "../Metadata/files.csv"

        # get all data from all files
        dene_files.set_all([media_path, rsync_path], locations_path, monitor_path, sessions_path)
        # then check everything
        dene_files.check_all()
        # finally complete files.csv
        dene_files.autocomplete(files_path, [media_path, rsync_path])

    elif args.media:
        # get and set file names in the media folder
        dene_files.set_media(args.media)
        # check the file names from the media folder
        dene_files.media_check()

        if args.files:
            # autocomplete files.csv
            dene_files.autocomplete(args.files, args.media)

        if args.sessions:
            # get and set session codes from sessions.csv
            dene_files.set_sessions(args.sessions)
            # check sessions.csv <-> media folder
            dene_files.compare_sessions_media()

        if args.locations:
            # get and set file names from locations.csv
            dene_files.set_locations(args.locations)
            # check media folder <-> locations.csv
            dene_files.compare_locations_media()

            if args.monitor:
                # get and set recording codes from monitor.csv
                dene_files.set_monitor(args.monitor)
                # check locations.csv <-> monitor.csv
                dene_files.compare_locations_monitor()

    else:

        if args.locations and args.monitor:
            # get and set recording codes from locations.csv
            dene_files.set_locations(args.locations)
            # get and set recording codes from monitor.csv
            dene_files.set_monitor(args.monitor)
            # check locations.csv <-> monitor.csv
            dene_files.compare_locations_monitor()

        else:
            print("You have not given the right combination of files via command line. Try again.")



    # close logging file
    handler.close()
