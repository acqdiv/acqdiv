from itertools import groupby

from pyacqdiv.util import read_csv, write_csv


def write_participants(corpus):
    """Extracts participants data from ids.csv into participants.csv.

    :return: path of the participants file
    """
    inrows = read_csv(corpus.cfg_path('ids.csv'), skip_header=False)
    cols = {name: index for index, name in enumerate(inrows[0])}
    outrows = [['filename', '@Participants:']]

    for fname, rows in groupby(sorted(inrows[1:]), key=lambda row: row[cols['filename']]):
        outrows.append([
            fname.replace(' ', ''),
            ', '.join('%s %s %s' % (r[cols['code']], r[cols['name']], r[cols['role']])
                      for r in rows)])

    return write_csv(corpus.cfg_path('participants.csv'), outrows)
