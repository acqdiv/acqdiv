import csv


class MorphemeMappingCSVParser:

    @staticmethod
    def parse(path, raw_pos=0, mapped_pos=1):
        morpheme_dict = {}

        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for row in reader:
                raw = row[raw_pos]
                mapped = row[mapped_pos]

                morpheme_dict[raw] = mapped

        return morpheme_dict

    @classmethod
    def parse_gloss(cls, path):
        return cls.parse(path)

    @classmethod
    def parse_pos(cls, path):
        return cls.parse(path)

    @classmethod
    def parse_pos_ud(cls, path):
        return cls.parse(path, mapped_pos=2)
