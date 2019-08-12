import csv


class MorphemeMappingCSVParser:

    @staticmethod
    def parse(path):
        morpheme_dict = {}

        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for row in reader:
                raw, mapped = row

                morpheme_dict[raw] = mapped

        return morpheme_dict
