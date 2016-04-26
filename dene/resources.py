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

formatter = logging.Formatter("%(object_number)d|%(object_id)s|%(funcName)s|%(levelname)s|%(message)s")
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
        self.media_file = os.path.split(self.path)[1]
        # store (lowercased) extension of media file
        self.extension = self.media_file[-3:].lower()
        # store parsed media file by exiftool
        self.et = et.get_metadata(self.path)


    def get_Session_code(self):
        """Strip of the dot and the file extension of the media file's name and return it."""
        return self.media_file[:-4]


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
            logger.error("Media file cannot be parsed by exiftool",
                extra={"object_number": 0, "object_id": self.media_file})
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
            logger.error("Media file cannot be parsed by exiftool",
                extra={"object_number": 0, "object_id": self.media_file})
            return ""
        else:
            return bytes


    def get_Word_size(self):
        """Not yet implemented."""
        return ""


    def get_Location(self):
        """Return absolute path of media file."""
        return "smb://server.ivs.uzh.ch/Dene/Media/" + self.media_file


    def in_media_dict(self):
        """Check if the file has one of the following extensions: wav, mp4, mts, mov. Return True or False."""
        return self.extension in Resource.media_dict


    def in_session_table(self):
        """Check if the file has an entry in the session table."""

    def in_media_folder(self):
        """Check if an entry in the sessions table has at least one corresponding file in the media folder"""


    def has_three_extension_types(self):


if __name__ == "__main__":

    # open resource file
    resource_file = open("../Metadata/resources.csv", "w+")
    # open session file
    session_file = open("../Metdata/sessions.csv", "r")

    # Dict reader instance for sessions
    sessions_reader = csv.DictReader(session_file, delimiter=",", quotechar='"')
    # Dict reader instance for resources
    resources_reader = csv.DictReader(resource_file, delimiter=",", quotechar='"')

    # store all session codes as a set
    session_codes = {row["Session code"] for row in sessions_reader}
    # store all media files in the resource table
    files_in_resources_table = {row["Session code"] for row in resources_reader}

    # our data structure for the files in the media folder:
    # {abstract_session_code: {session-A: {file.mov, file.mts, file.wav}, session-B: {file.mov, ....}}}
    files_in_media_folder = defaultdict(defaultdict(set))

    # create DictWriter instance for the new resources
    resources_writer = csv.DictWriter(resource_file,
    fieldnames=["Session code", "Type", "Format", "Duration", "Byte size", "Word size", "Location"])

    # create an exiftool instance to extract the metadata of the new resources
    with exiftool.ExifTool() as et:

        print(media_file) # just to see the progress...

        # Go through all media files in the media folder
        for media_file in os.listdir("test/Media"):

            # if the media file (without file extension) is not listed in the resources table
            if not media_file[:-4] in files_in_resources_table:

                # create an instance of the Resource class
                resource = Resource(path + "/" + media_file, et)

                # if the file is a hidden file, ignore it
                if media_file.startswith("."):
                    logger.warning("File '" + media_file + "' is a hidden file",
                    extra={"object_number": 0, "object_id": media_file})
                    break

                    # and then exclude any files that do not have the proper extension
                elif resource.in_media_dict():

                    # write data of the resource to the file 'resources.csv'
                    resources_writer.writerow({"Session code": resource.get_Session_code(),
                    "Type": resource.get_Type(),
                    "Format": resource.get_Format(),
                    "Duration": resource.get_Duration(),
                    "Byte size": resource.get_Byte_size(),
                    "Word size": resource.get_Word_size(),
                    "Location": resource.get_Location()
                    })

                else:
                    logger.warning("File '" + media_file + "' has unknown file extension",
                    extra={"object_number": 0, "object_id": media_file})
                    break

            # regex for checking and extracting (abstract) session name
            session_code_regex = re.compile(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-([A-Z]+|\d+|\d+[A-Z]+))?")

            # check if the session code is in the right format
            if session_code_regex.fullmatch(media_file):

                # get the abstract session code name for the media file
                abstract_session_code = re.search(r"deslas\-[A-Z]{3,}\-\d\d\d\d\-\d\d\-\d\d(\-\d+|)?").group()

                #TODO: implement right data structure
                files_in_media_folder[abstract_session_code].append(media_file)

                # check if the abstract session code is in the sessions table
                if abstract_session_code not in session_codes:
                    logger.error("Media file is not listed in the sessions table",
                        extra={"object_number": 0, "object_id": media_file})

            else:
                logger.error("Error in Session code", extra={"object_number": 0, "object_id": media_file})



            resource_file.close()
            session_file.close()

            for session_code in session_codes:

                if session_code in
