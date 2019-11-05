import csv


def parse_csv(path, raw_pos=0, mapped_pos=1):
    morpheme_dict = {}

    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            raw = row[raw_pos]
            mapped = row[mapped_pos]

            morpheme_dict[raw] = mapped

    return morpheme_dict


def parse_pos_ud(path):
    return parse_csv(path, mapped_pos=2)
