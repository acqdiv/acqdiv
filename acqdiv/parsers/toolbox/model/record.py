

class Record:

    def __init__(self):
        self.tiers = {}

    def get(self, field, not_exists=''):
        return self.tiers.get(field, not_exists)

    def __getitem__(self, field):
        return self.tiers.get(field, '')

    def __setitem__(self, key, value):
        self.tiers[key] = value

    def __iter__(self):
        for tier in self.tiers:
            yield tier

    def __contains__(self, field):
        return field in self.tiers
