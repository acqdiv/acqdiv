import csv

from acqdiv.util.util import get_full_path


def parse():
    """Return durations from session_durations.csv.

    Returns:
        Dict[Dict[str]]: The duration indexed by corpus and source_id.
    """
    durations_csv_path = 'ini/session_durations.csv'
    full_path = get_full_path(durations_csv_path)

    durations = {}

    with open(full_path, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            corpus = row['corpus']
            source_id = row['source_id']
            duration = row['duration']

            if corpus in durations:
                durations[corpus][source_id] = duration
            else:
                durations[corpus] = {source_id: duration}

    return durations


class SessionsDurationExtractor:

    durations = parse()

    @classmethod
    def extract(cls, corpus, source_id):
        """Get the duration.

        Args:
            corpus (str): The corpus name.
            source_id (str): The session name.
        """
        if corpus in cls.durations and source_id in cls.durations[corpus]:
            return cls.durations[corpus][source_id]

        return ''
