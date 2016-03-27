############################
## Installation of exiftool wrapper for python:
## git clone git://github.com/smarnach/pyexiftool.git
## sudo python3 setup.py install
############################

import sys, os, csv, logging, exiftool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("resources.log", mode="w")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(object_number)d|%(levelname)s|%(message)s")
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

        self.media_file = os.path.split(path)[1]
        self.extension = self.media_file[-3:].upper()

        self.type = self.type = Resource.media_dict[self.extension][0]
        self.format = Resource.media_dict[self.extension][0] + "/" + self.extension
        self.location = "Dene/Media/" + self.media_file
        self.session_code = self.media_file[:-4]
        self.word_size = ""

        # exiftool used for extracting byte size and duration of file
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata(path)

            self.byte_size = metadata["File:FileSize"]

            # set duration
            duration_in_seconds = metadata[Resource.media_dict[self.extension][1] + ":Duration"]
            m, s = divmod(duration_in_seconds, 60)
            h, m = divmod(m, 60)
            self.duration = "%02d:%02d:%02d" % (h, m, s)


    def in_media_dict(self):
        return self.extension in Resource.media_dict



if __name__ == "__main__":

    path = sys.argv[1]

    resource_file = open("resources.csv", "w")

    fields_resource = ["Session code", "Type", "Format", "Duration", "Byte size", "Word size", "Location"]

    writer = csv.DictWriter(resource_file, fieldnames=fields_resource)
    writer.writeheader()

    for media_file in os.listdir(path):
        resource = Resource(path + "/" + media_file)

        writer.writerow({"Session code": resource.session_code,
                        "Type": resource.type,
                        "Format": resource.format,
                        "Duration": resource.duration,
                        "Byte size": resource.byte_size,
                        "Word size": resource.word_size,
                        "Location": resource.location
                        })
