"""Extracts the metadata for resources and checks the recording files on the server.

This modules includes two classes, one extracting metadata from resources and one checking the whole file system on the server.
If you run this module, make sure exiftool (http://www.sno.phy.queensu.ca/~phil/exiftool/) and
the python wrapper for it (https://smarnach.github.io/pyexiftool/) is installed.

The script should be located in a folder named "Scripts" whereas the files to be checked should be in a folder named "Media"
located on the same level. If these conditions are given, simply run python3 system_check.py
"""

import os
import re
import csv
import sys
import argparse
import logging
import exiftool
from collections import defaultdict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("resources.log", mode="w")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(object_id)s|%(funcName)s|%(levelname)s|%(message)s")
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

    def __init__(self, path, et):
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
        self.et = et.get_metadata(self.path)


    def get_Session_code(self):
        """Strip off extension part and any letters for partial sessions and return it"""
        match = re.search(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d+|)?", self.file_name)

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
            duration_in_secs = self.et[Resource.media_dict[self.extension][1] + ":Duration"]
        except KeyError:
            logger.error("Duration cannot be extracted by exiftool", extra={"object_id": self.file_name})
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
            bytes = self.et["File:FileSize"]
        except KeyError:
            logger.error("Byte size cannot be extracted by exiftool", extra={"object_id": self.file_name})
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
        # data structure for system: {session_code: {rec_code_A: {file.mp4, file.mts/mov, file.wav}, rec_code_B: {file.mov, ....}, ...}, ...}
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

            else:
                logger.error("Format of recording code wrong", extra={"object_id": rec})


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


    def set_all(media_path, locations_path, monitor_path, sessions_path):
        """Gets and sets all data.

        Positional args:
            media_path: path to media folder
            locations_path: path to file_locations.csv
            monitor_path: path to monitor.csv
            sessions_path: path to sessions.csv
        """
        set_media(media_path)
        set_locations(locations_path)
        set_monitor(monitor_path)
        set_sessions(sessions_path)


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
            n_recs = str(len(new_recs))
            counter = 0

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
                        "Session code": get_Session_code(),
                        "Recording code": get_Recording_code(),
                        "File name": rec,
                        "Type": resource.get_Type(),
                        "Format": resource.get_Format(),
                        "Duration": resource.get_Duration(),
                        "Byte size": resource.get_Byte_size(),
                        "Word size": resource.get_Word_size(),
                        "Location": resource.get_Location()
                    })

                # if file is a hidden file, produce warning
                elif rec.startswith(".") and rec != ".DS_Store":
                    logger.warning("File '" + rec + "' is a hidden file", extra={"object_id": rec})

                else:
                    logger.warning("File '" + rec + "' has unknown file extension", extra={"object_id": rec})



    def media_check(self):
        """Checks consistency of recording files in the Media folder.

        The following checks are made:
            - consecutive letters in recording codes
            - consecutive numbers in session codes
            - every recording code occurs with a wav, mp4 and mts/mov extension
        """

        # hash storing session codes mapped to a list with (ideally) consecutive numbers
        same_day_session_codes = defaultdict(list)

        # Go through all session codes
        for session_code in self.media_structure:

            # Check if it has same-day-session-number and save number with this session_code
            match = re.search(r"(.*\d\d\d\d\-\d\d\-\d\d)\-(\d+)$", session_code)
            if match:
                part_without_number = match.group(1)
                number = int(match.group(2))
                same_day_session_codes[part_without_number].append(number)

            # create list of (ideally) consecutive letters
            letter_seq_list = []

            # Go through all recording codes mapped to that session code
            for rec_code in self.media_structure[session_code]:

                # extract partial code letter
                match = re.search(r"[A-Z]+$", rec_code)
                if match:
                    letter_seq_list += list(match.group())

                three_files_check(rec_code, self.media_structure[session_code][rec_code])

            consecutive_letter_check(session_code, letter_seq_list)

        consecutive_number_check(same_day_session_codes)



    def three_files_check(self, rec_code, rec_set):
        """Checks if every recording code occurs with a wav, mp4 and mts/mov extension.

        positional args:
            rec_code: recording code under which the three files are subsumed
            rec_set: (ideally) contains three different file types
        """
        # Check if file with wav-extension exists
        if rec_code + ".wav" not in rec_set:
            logger.error("wav-file missing for: " + rec_code, extra={"object_id": rec_code})

        # Check if file with mp4-extension exists
        if rec_code + ".mp4" not in rec_set:
            logger.error("mp4-file missing for: " + rec_code, extra={"object_id": rec_code})

        # Check if file with mov/mts-extension exists
        if rec_code + ".mts" not in rec_set and rec_code + ".mov" not in rec_set:
            logger.error("mov/mts-file missing for: " + rec_code, extra={"object_id": rec_code})


    def consecutive_letter_check(self, session_code, letter_seq_list):
        """Checks if letters are consecutive.

        Positional args:
            session_code: session code under which the recording codes are subsumed
            letter_seq_list: list containing letters
        """
        if letter_seq_list:

            # first sort letters
            letter_seq_list = sorted(letter_seq_list)

            # Check if letters are consecutive in this list
            counter = 0
            for letter in letter_seq_list:

                # get desired letter
                should_be_letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[counter]

                # check if desired letter corresponds to the letter in the list
                if letter != should_be_letter:
                    logger.error("Recording codes of " + session_code + " are not consecutive - recording code " + session_code + should_be_letter + " missing", extra={"object_id": session_code})

                    counter += 2
                else:
                    counter += 1


    def consecutive_number_check(self, same_day_codes):
        """Check if same-day-session codes are consecutive.

        positional args:
            same_day_codes: hash mapping session code to a list of numbers
        """
        # go through all session codes
        for session_code in same_day_codes:

            # first sort all numbers
            numbers = sorted(same_day_codes[session_code])

            counter = 1
            for number in numbers:

                if number != counter:
                    logger.error("Same-day-sessions of " + session_code + "are not consecutive - session code " + code + str(counter) + " missing",
                    extra={"object_id": code})

                    counter += 2
                else:
                    counter += 1


    def compare_sessions_media(self):
        """Check if every session code in sessions.csv has at least one file in the media folder and vice versa."""
        # Check session.csv -> media folder
        for session_code in self.session_codes_from_sessions:
            if session_code not in self.media_structure:
                logger.warning(session_code + " from sessions.csv not in media folder", extra={"object_id": session_code})

        # Check media folder -> sessions.csv
        for session_code in self.media_structure:
            if session_code not in self.session_codes_from_sessions:
                logger.error(session_code + " from media folder not in sessions.csv", extra={"object_id": session_code})


    def compare_locations_media(self):
        """Check if every recording name in file_locations.csv has a corresponding file in the media folder and vice versa."""
        # Check file_locations.csv -> media folder
        for rec in self.recs_from_file_locations - self.recs_from_media_folder:
            logger.error(rec + " from file_locations.csv not in media folder", extra={"object_id": rec})

        # Check media folder -> file_locations.csv
        for rec in self.recs_from_media_folder - self.recs_from_locations:
            logger.error(rec + " from media folder not in file_locations.csv", extra={"object_id": rec})


    def compare_locations_monitor(self):
        """Check if every recording code in file_locations.csv is also listed in monitor.csv and vice versa."""
        # Check file_locations.csv -> monitor.csv
        for rec in self.rec_codes_from_locations - self.rec_codes_from_monitor:
            logger.error(rec + " from file_locations.csv not in file_locations.csv", extra={"object_id": rec})

        # Check monitor.csv -> file_locations.csv
        for rec in self.rec_codes_from_monitor - self.rec_codes_from_locations:
            logger.error(rec + " from monitor.csv not in file_locations.csv", extra={"object_id": rec})


    def check_all(self):
        """Checks whole system."""
        media_check()
        compare_sessions_media()
        compare_locations_media()
        compare_locations_monitor()


if __name__ == "__main__":

    # get all arguments from the command line
    arg_list = sys.argv

    # default settings if no argument were given
    if len(arg_list) == 1:

        media_path = "../Media"
        locations_path = "../Workflow/file_locations.csv"
        monitor_path = "../Workflow/monitor.csv"
        sessions_path = "../Metadata/sessions.csv"
        resources_path = "../Metadata/resources.csv"

        dene_recs = System_check()
        dene_recs.set_all(media_path, locations_path, monitor_path, sessions_path)
        dene_recs.check_all()
        dene_recs.autocomplete(resources_path, media_path)


    handler.close()
