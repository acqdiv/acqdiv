import sys, os, csv, logging, exiftool, datetime, metadata

############################
## exiftool is used for extracting metadata of media files
## Installation of exiftool wrapper for python:
## git clone git://github.com/smarnach/pyexiftool.git
## sudo python3 setup.py install
############################

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("resources.log", mode="w")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(levelname)s|%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Resource:

    media_dict = {
                "WAV": ("Audio", "Composite"),
                "MP4": ("Video", "QuickTime"),
                "MTS": ("Video", "M2TS"),
                "MOV": ("Video", "QuickTime")
    }

    def __init__(self, path):

        self.path = path
        self.media_file = os.path.split(path)[1]
        self.extension = self.media_file[-3:].upper()


    def get_session_code(self):
        return self.media_file[:-4]


    def get_type(self):
        return Resource.media_dict[self.extension][0]


    def get_format(self):
        return Resource.media_dict[self.extension][0] + "/" + self.extension


    def get_duration(self, session_file):

        with exiftool.ExifTool() as et:

            duration_in_secs = et.get_metadata(self.path)[Resource.media_dict[self.extension][1] + ":Duration"]

            time_from_mediafile = datetime.timedelta(seconds=duration_in_secs)

            reader = csv.DictReader(session_file, delimiter=",", quotechar='"')

            for row in reader:
                if row["Code"] == get_session_code():
                    len_of_rec = row["Length of recording"]

                    if re.search(r"\d{1,2}:\d{1,2}:\d{1,2}", len_of_rec):
                        h, m, s = len_of_rec.split(":")

                        time_from_table = datetime.timedelta(hours=h, minutes=m, seconds=s)

                        threshold = datetime.timedelta(minutes=3)

                        if abs(time_from_mediafile - time_from_table) > threshold:
                            logger.warning("Length recording times deviate too much: " + row["Code"])

                        return "%02d:%02d:%02d" % (h, m, s)

            return ""


    def get_byte_size(self):

        with exiftool.ExifTool() as et:
            return et.get_metadata(self.path)["File:FileSize"]


    def get_word_size(self):
        return ""


    def get_location(self):
        return "Dene/Media/" + self.media_file


    def in_media_dict(self):
        return self.extension in Resource.media_dict

    def check_Code(self, session_file):
        reader = csv.DictReader(session_file, delimiter=",", quotechar='"')

        for row in reader:
            if row[Code] == get_session_code():
                break
        else:
            logger.warning("Media File " + get_session_code() + " does not occur in session table")

    def correct_filename(self, participant_file):
        code = get_session_code()
        session = Session()
        session.code = code
        session.check_Code()

        os.rename(self.media_file, session.code + "." + self.extension)



if __name__ == "__main__":

    path = "./TestFiles"

    resource_file = open("resources.csv", "w")
    session_file = open("sessions.csv", "r")

    fields_resource = ["Session code", "Type", "Format", "Duration", "Byte size", "Word size", "Location"]

    writer = csv.DictWriter(resource_file, fieldnames=fields_resource)
    writer.writeheader()

    for media_file in os.listdir(path):
        resource = Resource(path + "/" + media_file)

        if resource.in_media_dict():

            writer.writerow({"Session code": resource.get_session_code(),
                            "Type": resource.get_type(),
                            "Format": resource.get_format(),
                            "Duration": resource.get_duration(),
                            "Byte size": resource.get_byte_size(),
                            "Word size": resource.get_word_size(),
                            "Location": resource.get_location()
                            })

        else:
            logger.warning("File '" + media_file + "' has unknown file extension")
