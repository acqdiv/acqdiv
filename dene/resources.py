"""Extracts the metadata for resources.

This modules implements a class for extracting the metadata of resources with the help of ExifTool.

To run the script externally, do the following:
>sudo mkdir test
>sudo mount -t cifs //server.ivs.uzh.ch/Dene test/ -o user=<your_username>
>python3 resources.py

Make sure the path to the media files is correct (line 130).
Do not forget to unmount when you are done:
>sudo umount test/
"""

import os
import re
import csv
import logging
import exiftool
from collections import defaultdict

#################################################################
## exiftool is used for extracting the metadata of media files
## Installation of exiftool:
## sudo apt-get install libimage-exiftool-perl perl-doc
## Installation of exiftool wrapper for python:
## git clone git://github.com/smarnach/pyexiftool.git
## sudo python3 setup.py install
#################################################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("resources.log", mode="w")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(object_id)s|%(funcName)s|%(levelname)s|%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


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


if __name__ == "__main__":

    # open resource file for reading and writing data
    resource_file = open("resources.csv", "r+")
    # open session file for reading data
    session_file = open("test/Metadata/sessions.csv", "r")

    # Dict reader instance for sessions
    sessions_reader = csv.DictReader(session_file, delimiter=",", quotechar='"')
    # Dict reader instance for resources
    resources_reader = csv.DictReader(resource_file, delimiter=",", quotechar='"')

    # store all session codes from the sessions table in a set
    session_codes = {row["Code"] for row in sessions_reader}
    # store all recording files from the resource table in a set
    recs_from_resources_table = {row["File name"] for row in resources_reader}

    # data structure for saving the recording files in the media folder
    # {session_code: {recording_code_A: {file.mp4, file.mts/mov, file.wav}, recording_code_B: {file.mov, ....}}}
    rec_hash = defaultdict(lambda: defaultdict(set))

    # create DictWriter instance for the new resources
    resources_writer = csv.DictWriter(resource_file, fieldnames=["Session code", "Recording code", "File name", "Type",
                                                                "Format", "Duration", "Byte size", "Word size", "Location"])
    # TODO: überprüfen, ob parial codes fortlaufend sind
    # TODO: überprüfen, ob session-code-1, session-code2 vorhanden
    # TODO: file_locations.xls checking -> only where yes for UZH
    # TODO: monitor -> file_locations and file_locations -> monitor || monitor (Teilmenge von file_locations)


    ######################################################################################################################################

    ############### Checks for resources.csv ##########################

    # path to the media files
    resources = os.listdir("test/Media")

    # used to see progress of script
    number_of_resources = str(len(resources))
    counter = 0

    # Go through all recording files in the media folder
    for rec in resources:

        counter += 1

        print(rec + "\t\t\t" + str(counter) + "/" + number_of_resources) # just to see the progress

        # get recording code for that recording file by stripping off file extension
        rec_code = rec[:-4]

        # regex for checking and extracting parts of the recording code
        rec_code_regex = re.compile(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-([A-Z]+|\d+|\d+[A-Z]+))?")

        # check the format of the recording code
        if rec_code_regex.fullmatch(rec_code):

            # infer the session code for that recording file
            session_code = re.search(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d+|)?", rec_code).group()

            # store recording file under the right session and recording code
            rec_hash[session_code][rec_code].add(rec)

            # if the recording file is not listed in the resources table
            if rec not in recs_from_resources_table:

                # create an exiftool instance to extract the metadata of that recording file
                with exiftool.ExifTool() as et:

                    # create an instance of the Resource class
                    resource = Resource("test/Media/" + rec, et)

                    # and then exclude any files that do not have the proper extension
                    if resource.in_media_dict():

                        # write metadata to the file 'resources.csv'
                        resources_writer.writerow({
                            "Session code": session_code,
                            "Recording code": rec_code,
                            "File name": rec,
                            "Type": resource.get_Type(),
                            "Format": resource.get_Format(),
                            "Duration": resource.get_Duration(),
                            "Byte size": resource.get_Byte_size(),
                            "Word size": resource.get_Word_size(),
                            "Location": resource.get_Location()
                        })

                    else:
                        logger.warning("File '" + rec + "' has unknown file extension", extra={"object_id": rec})


        # if the file is a hidden file, ignore it and produce warning
        elif rec.startswith("."):
            if rec != ".DS_Store":
                logger.warning("File '" + rec + "' is a hidden file", extra={"object_id": rec})

        else:
            logger.error("Format of recording code wrong", extra={"object_id": rec})


    # Go through all session codes that were inferred from the recording names in the media folder
    for session_code in rec_hash:

        # check if the session code is listed in the sessions table
        if session_code not in session_codes:
            logger.error("Session code is not listed in the sessions table", extra={"object_id": session_code})

        # Go through all recording codes mapped to that session code
        for rec_code in rec_hash[session_code]:

            # store set containing all recs mapped to that recording code
            rec_set = rec_hash[session_code][rec_code]

            # Check if audio file exists for that recording code
            if rec_code + ".wav" not in rec_set:
                logger.error("Audio file with wav-extension missing for: " + rec_code, extra={"object_id": rec_code})

            # Check if video file with mp4-extension exists for that recording code
            if rec_code + ".mp4" not in rec_set:
                logger.error("Video file with mp4-extension missing for: " + rec_code, extra={"object_id": rec_code})

            # Check if video file with mov/mts-extension exists for that recording code
            if rec_code + ".mts" not in rec_set and rec_code + ".mov" not in rec_set:
                logger.error("Video file with mov/mts-extension missing for: " + rec_code, extra={"object_id": rec_code})


    # Go through all session codes from the sessions table
    for session_code in session_codes:

        # Check if that session code has at least one recording file in the media folder
        if session_code not in rec_hash:
            logger.warning("No recording file in Media folder for session code: " + session_code, extra={"object_id": session_code})



    ######################################################################################################################################







    resource_file.close()
    session_file.close()
    handler.close()
