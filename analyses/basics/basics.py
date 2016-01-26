import sqlite3
import pandas as pd
import sys


def ngrams(words, n=2):
    """Returns ngrams
    Args:
        words: a list of strings, e.g. ['a', 'b', 'c', 'd']
        n: int ngram length
    Returns: list of tuples where ngram = len(n), e.g. [('a', 'b'), ('b', 'c'), ...]
    """
    """ TODO: deal with missing grams?
    if len(words) < n:
        result = []
        for i in range(len(n)):
            result.append(words[i])
        return
    """
    return list(zip(*[words[i:] for i in range(n)]))


def main():
    """ Performs data manipulation and number crunching for networks analysis
    """
    # get data (is ordering important?)

    con = sqlite3.connect("../../database/_acqdiv.sqlite3")
    df = pd.read_sql_query('SELECT * from morphemes', con)
    print(df.head())
    # sys.exit(1)


    df = pd.read_sql_query('select utterances.utterance, utterances.pos_raw '
                              'from utterances, speakers ', con)





    """
    df = pd.read_sql_query(
        'SELECT utterances.id as ID, sessions.date, utterances.utterance, speakers.speaker_label, '
        'speakers.age_in_days, sessions.corpus '
        'FROM speakers '
        'INNER JOIN utterances '
        'ON utterances.session_id_fk = speakers.session_id_fk '
        'INNER JOIN sessions '
        'ON sessions.session_id = utterances.session_id_fk '
        'WHERE speakers.speaker_label = "ALJ" AND sessions.corpus = "Russian" '
        'AND role_raw = "Target_Child"'
        'ORDER BY ID', con)

    # add new columns to df, including split utterances, their lengths and bigrams
    df['words'] = df['utterance'].str.split()
    df['utterance_length'] = df['words'].str.len()
    df['bigrams'] = df['words'].apply(ngrams)

    print(df.head())
    """

if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print()
    print("--- %s seconds ---" % (time.time() - start_time))