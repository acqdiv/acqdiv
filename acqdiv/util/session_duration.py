import csv

from acqdiv.util.path import get_full_path


def _parse():
    """Return durations from session_durations.csv.

    Returns:
        Dict[Dict[str]]: The duration indexed by corpus and source_id.
    """
    durations_csv_path = 'util/resources/session_durations.csv'
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


_durations = _parse()


def extract_duration(corpus, source_id):
    """Get the duration.

    Args:
        corpus (str): The corpus name.
        source_id (str): The session name.

    Returns:
        str: The duration.
    """
    if corpus in _durations and source_id in _durations[corpus]:
        return _durations[corpus][source_id]

    return ''
