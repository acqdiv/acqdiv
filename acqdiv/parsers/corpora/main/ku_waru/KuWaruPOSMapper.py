from acqdiv.util.MorphemeMappingCSVParser import MorphemeMappingCSVParser


class KuWaruPOSMapper:

    def __init__(self, path):
        self.pos_dict = MorphemeMappingCSVParser.parse(path)

    def map(self, raw):
        return self.pos_dict[raw]
