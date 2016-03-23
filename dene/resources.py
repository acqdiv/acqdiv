import os, csv

class Resource:

    media_dict = {"wav": "Audio", "mp4": "Video", "mts": "Video", "MOV": "Video"}

    def __init__(self):

        self.session_code = ""
        self.type = ""
        self.format = ""
        self.duration = ""
        self.byte_size = ""
        self.word_size = ""
        self.location = ""


    def set_Type(self):
        pass

    def set_sessionCode(self):
        pass

    def set_format(self):
        pass

    def set_duration(self):
        pass

    def set_byteSize(self):
        pass

    def set_wordSize(self):
        pass

    def set_location(self):
        pass


if __name__ == "__main__":

    resource_file = open("resources.csv", "a")

    fields_resource = ["Session code", "Type", "Format", "Duration", "Byte size", "Word size", "Location"]

    writer = csv.DictWriter(resource_file, fieldnames=fields_resource)

    for media in os.listdir():
        pass

    writer.writerow({"Session code": self.session_code,
                    "Type": self.type,
                    "Format": self.format,
                    "Duration": self.duration,
                    "Byte size": self.byte_size,
                    "Word size": self.word_size,
                    "Location": self.location
                    })
