# Use `compare_database_stats.py` to compare two versions of the acqdiv
# database.
# Files generated:
# 1. Metrics like number of words and number of morphemes are computed
# for both input databases and the difference scaled to 0-1 is calculated.
# These metrics are calculated for each corpus individually and for all
# corpora, that exist in both databases (corpus = global).
# The output is a csv-file with name *corpus_stats.csv*
# and the columns
# *corpus, table, measure, db1, db2, difference*.
#
# 2. The number of occurrences of all words per corpus is
# computed. The output is a csv-file with name
# *words_per_corpus_stats.csv* and the columns
# *corpus, word, num_in_db1, num_in_db2, diff*.
#
# 3. The number of occurrences of all morphemes per corpus is
# computed. The output is a csv-file with name
# *morphemes_per_corpus_stats.csv*
# and the columns
# *corpus, morpheme, num_in_db1, num_in_db2, diff*.
#
# 4. The number of occurrences of all glosses per corpus is
# computed. The output is a csv-file with name
# *glosses_per_corpus_stats.csv*
# and the columns
# *corpus, glosses, num_in_db1, num_in_db2, diff*.
#
# 5. The number of occurrences of all poses per corpus is
# computed. The output is a csv-file with name
# *poses_per_corpus_stats.csv*
# and the columns
# *corpus, poses, num_in_db1, num_in_db2, diff, in_manual*.
#
# Usage:
# To generate the tables with all frequencies computed:
# ```
# python3 compare_database_stats.py -db1 <path_to_db1> -db2 <path_to_db2>
# ```
# To generate the tables with only the frequencies where the two DBs
# differ from each other:
# ```
# python3 compare_database_stats.py -db1 <path_to_db1> -db2 <path_to_db2> -od
# ```
#
# `db1` and `db2` are sqlite3-files.
#
# `-od` only write rows to file where there is a difference.
#
# The script only generates statistics for corpora that exist in
# both databases. All corpora that only exist in one of the databases
# are ignored (they also also not included in the global statistics).
#
# If the database hasn't gone through postprocessing the pos- and
# gloss-tables are empty since they haven't yet been inferred.
#
# If the two databases have no corpora in common the sql-queries become
# invalied and the script will crash!

import csv
import sqlalchemy as sa
import argparse
from collections import defaultdict


poses = ['ADJ', 'ADV', 'ART', 'AUX', 'CLF', 'CONJ',
         'IDEOPH', 'INTJ', 'N', 'NUM', 'pfx', 'POST', 'PREP',
         'PRODEM', 'PTCL', 'PVB', 'QUANT', 'sfx', 'stem', 'V']


# ---------- Helper Functions ----------


def setup():
    """Parse cmd-args and create db-connections."""
    global conn1, conn2, od

    parser = argparse.ArgumentParser()
    parser.add_argument('-db1')
    parser.add_argument('-db2')
    parser.add_argument('-od', action='store_true')
    args = parser.parse_args()

    sql_path_db1 = 'sqlite:///{}'.format(args.db1)
    sql_path_db2 = 'sqlite:///{}'.format(args.db2)
    od = args.od

    engine1 = sa.create_engine(sql_path_db1)
    engine2 = sa.create_engine(sql_path_db2)

    conn1 = engine1.connect()
    conn2 = engine2.connect()


def get_common_corpora():
    """Return all corpora that exist in both databases."""
    query = r'SELECT DISTINCT(corpus) FROM utterances;'
    corpora_1 = [n[0] for n in conn1.execute(query)]
    corpora_2 = [n[0] for n in conn2.execute(query)]
    common_corpora = []
    for c in corpora_1:
        if c in corpora_2:
            common_corpora.append(c)
    return common_corpora


def get_corpus_cond(corpora):
    """Format all input corpora to a sql-query condition."""
    corpus_cond = '('
    for i in range(len(corpora)):
        corpus = corpora[i]
        corpus_cond += "corpus = '{}' ".format(corpus)
        if i != len(corpora)-1:
            corpus_cond += 'or '
    corpus_cond += ')'
    return corpus_cond


def get_query_results(query):
    """Send query to the two DBs and fetch results."""
    results1 = list(conn1.execute(query))[0][0]
    results2 = list(conn2.execute(query))[0][0]
    return results1, results2


def get_difference(i, j):
    """Compute how much j deviates from i scaled from 0 to 1."""
    if i != 0:
        diff = i - j
        diff_scaled = abs(diff / i)
    elif j != 0:
        diff = j - i
        diff_scaled = abs(diff / j)
    else:
        diff_scaled = 0
    return diff_scaled


# ---------- Global Statistics ----------


def get_corpus_statistics(corpora):
    """Get the cumulative statistics for the given list of corpora."""
    d = {'uniquespeakers': get_uniquespeakers_stats(corpora),
         'speakers': get_speakers_stats(corpora),
         'sessions': get_sessions_stats(corpora),
         'utterances': get_utterances_stats(corpora),
         'words': get_words_stats(corpora),
         'morphemes': get_morphemes_stats(corpora)}
    return d


# ---------- Unique Speakers ----------


def get_uniquespeakers_stats(corpora):
    d = {'num_uniquespeakers': get_num_uniquespeakers_uniquespeakers(corpora),
         'num_females': get_num_females_uniquespeakers(corpora),
         'num_males': get_num_males_uniquespeakers(corpora)}
    return d


def get_num_uniquespeakers_uniquespeakers(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = 'SELECT COUNT(*) FROM uniquespeakers WHERE {};'.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


def get_num_females_uniquespeakers(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = ("SELECT COUNT(*) FROM uniquespeakers "
             "WHERE {} and gender = 'Female';")
    query = query.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


def get_num_males_uniquespeakers(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = "SELECT COUNT(*) FROM uniquespeakers WHERE {} and gender = 'Male';"
    query = query.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


# ---------- Speakers ----------


def get_speakers_stats(corpora):
    d = {'num_speakers': get_num_speakers_speakers(corpora),
         'num_females': get_num_females_speakers(corpora),
         'num_males': get_num_males_speakers(corpora),
         'num_target_children': get_num_target_children(corpora)}
    return d


def get_num_speakers_speakers(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = 'SELECT COUNT(*) FROM speakers WHERE {};'.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


def get_num_females_speakers(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = "SELECT COUNT(*) FROM speakers WHERE {} and gender = 'Female';"
    query = query.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


def get_num_males_speakers(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = "SELECT COUNT(*) FROM speakers WHERE {} and gender = 'Male';"
    query = query.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


def get_num_target_children(corpora):
    corpus_cond = get_corpus_cond(corpora)
    query = ("SELECT COUNT(*) FROM speakers WHERE {} "
             "and macrorole = 'Target_Child';")
    query = query.format(corpus_cond)
    d = {}
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


# ---------- Sessions ----------


def get_sessions_stats(corpora):
    return {'num_sessions': get_num_sessions_sessions(corpora)}


def get_num_sessions_sessions(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = 'SELECT COUNT(*) FROM sessions WHERE {};'.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


# ---------- Utterances ----------


def get_utterances_stats(corpora):
    d = {'num_utterances': get_num_utterances_utterances(corpora)}
    return d


def get_num_utterances_utterances(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = 'SELECT COUNT(*) FROM utterances WHERE {};'.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


# ---------- Words ----------


def get_words_stats(corpora):
    d = {'num_words': get_num_words_words(corpora),
         'num_distinct_words': get_num_distinct_words_words(corpora)}
    # for pos in poses:
    #     d[pos] = get_num_pos_words(pos, corpora)
    return d


def get_num_words_words(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = 'SELECT COUNT(*) FROM words WHERE {};'.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


def get_num_distinct_words_words(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = 'SELECT COUNT(DISTINCT(word)) FROM words WHERE {};'
    query = query.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


# def get_num_pos_words(pos, corpora):
#     d = {}
#     corpus_cond = get_corpus_cond(corpora)
#     query = "SELECT COUNT(*) FROM words WHERE {} and pos = '{}';"
#     query = query.format(corpus_cond, pos)
#     d['db1'], d['db2'] = get_query_results(query)
#     d['difference'] = get_difference(d['db1'], d['db2'])
#     return d


# ---------- Morphemes ----------


def get_morphemes_stats(corpora):
    d = {'num_morphemes': get_num_morphemes_morphemes(corpora)}
    for pos in poses:
        d[pos] = get_num_pos_morphemes(pos, corpora)
    return d


def get_num_morphemes_morphemes(corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = 'SELECT COUNT(*) FROM morphemes WHERE {};'.format(corpus_cond)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


def get_num_pos_morphemes(pos, corpora):
    d = {}
    corpus_cond = get_corpus_cond(corpora)
    query = "SELECT COUNT(*) FROM morphemes WHERE {} and pos = '{}';"
    query = query.format(corpus_cond, pos)
    d['db1'], d['db2'] = get_query_results(query)
    d['difference'] = get_difference(d['db1'], d['db2'])
    return d


# ---------- Word Stats ----------


def results_to_dict(results):
    """Convert the results, a list of tuples to a dict."""
    d = defaultdict(dict)  # {corpus: {word: frequency}}
    for tpl in results:
        d[tpl[0]][tpl[1]] = tpl[2]
    return d


def merge(results1, results2):
    """Merge the two result-dicts into one dict.

    Args:
        results1, results2: A dict as produced by results_to_dict.
    Return:
        A dictionary of the form:
        {corpus: {elem: {db1: freq, db2: freq}}} with the types
        {str:    {str:  {str: int,  str: int}}}
        where elem is as string representing either a word, a morpheme,
        a gloss or a pos.
    """
    d = defaultdict(lambda: defaultdict(dict))
    # {corpus: {elem: {db1: freq, db2: freq}}}
    # Get results from db1 into d.
    for corpus in results1:
        results1_corpus = results1[corpus]
        for elem in results1_corpus:
            d[corpus][elem] = {'db1': results1_corpus[elem], 'db2': 0}
    # Get results from db2 into d.
    for corpus in results2:
        results2_corpus = results2[corpus]
        for elem in results2_corpus:
            if elem in d[corpus]:
                d[corpus][elem]['db2'] = results2_corpus[elem]
            else:
                d[corpus][elem] = {'db1': 0, 'db2': results2_corpus[elem]}
    return d


def get_query_results_elem_stats(query):
    results1 = results_to_dict(conn1.execute(query))
    results2 = results_to_dict(conn2.execute(query))
    return results1, results2


def calc_diff(elem_stats_both):
    for corpus in elem_stats_both:
        corp_stats = elem_stats_both[corpus]
        for elem in corp_stats:
            freq1 = corp_stats[elem]['db1']
            freq2 = corp_stats[elem]['db2']
            diff = get_difference(freq1, freq2)
            corp_stats[elem]['diff'] = diff
    return elem_stats_both


def get_word_stats(corpora):
    corpus_cond = get_corpus_cond(corpora)
    query = ('SELECT corpus, word, COUNT(word) FROM words '
             'GROUP BY corpus, word').format(corpus_cond)
    results1, results2 = get_query_results_elem_stats(query)
    words_stats_both = merge(results1, results2)
    word_stats_diff = calc_diff(words_stats_both)
    return word_stats_diff


# ---------- Morpheme Stats ----------


def get_morpheme_stats(corpora):
    """Get for each morpheme type the number of morphemes per corpus."""
    corpus_cond = get_corpus_cond(corpora)
    query = ('SELECT corpus, morpheme, COUNT(morpheme) FROM morphemes '
             'GROUP BY corpus, morpheme').format(corpus_cond)
    results1, results2 = get_query_results_elem_stats(query)
    morpheme_stats_both = merge(results1, results2)
    morpheme_stats_diff = calc_diff(morpheme_stats_both)
    return morpheme_stats_diff


# ---------- Gloss Stats ----------


def get_gloss_stats(corpora):
    """Get for each gloss type the numer of gloss per corpus."""
    corpus_cond = get_corpus_cond(corpora)
    query = ('SELECT corpus, gloss, COUNT(gloss) FROM morphemes '
             'GROUP BY corpus, gloss').format(corpus_cond)
    results1, results2 = get_query_results_elem_stats(query)
    gloss_stats_both = merge(results1, results2)
    gloss_stats_diff = calc_diff(gloss_stats_both)
    return gloss_stats_diff


# ---------- POS Stats ----------


def check_pos_in_manual(pos_stats_diff):
    """Create an additional column indicating if pos is in manual."""
    for corpus in pos_stats_diff:
        corp_stats = pos_stats_diff[corpus]
        for pos in corp_stats:
            corp_stats[pos]['in_manual'] = pos in poses
    return pos_stats_diff


def get_pos_stats(corpora):
    """Get for each pos type the numer of pos per corpus."""
    corpus_cond = get_corpus_cond(corpora)
    query = ('SELECT corpus, pos, COUNT(pos) FROM words '
             'GROUP BY corpus, pos').format(corpus_cond)
    results1, results2 = get_query_results_elem_stats(query)
    pos_stats_both = merge(results1, results2)
    pos_stats_diff = calc_diff(pos_stats_both)
    pos_stats_in_manual = check_pos_in_manual(pos_stats_diff)
    return pos_stats_in_manual


# ---------- File Writing ----------


def write_corpus_stats(stats):
    """Write data to 'corpus_stats.csv'.

    Column-names:
    corpus, table, measure, db1, db2, difference
    """
    with open('corpus_stats.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['corpus', 'table', 'measure',
                         'db1', 'db2', 'difference'])
        for cname in stats:
            cstats = stats[cname]
            for tname in cstats:
                tstats = cstats[tname]
                for measure in tstats:
                    mstats = tstats[measure]
                    val_db1 = mstats['db1']
                    val_db2 = mstats['db2']
                    diff = mstats['difference']
                    if od:
                        if diff != 0 and diff is not None:
                            row = [cname, tname, measure, val_db1, val_db2,
                                   diff]
                            writer.writerow(row)
                    else:
                        row = [cname, tname, measure, val_db1, val_db2, diff]
                        writer.writerow(row)


def write_elem_stats(elem_stats, elem_type):
    """Write stats for words/morphemes/glosses to file.

    The output-file is named '<elem>_per_corpus_stats.csv' where
    <elem> is either words, morphemes, glosses or poses.

    Args:
        elem_stats: {corpus: {elem: {db1: freq, db2: freq, diff: diff}}}
        elem_type: A string, either 'word', 'morpheme' or 'gloss'.

    Column names:
    corpus, <elem>, freq_db1, freq_db2, diff
    """
    fname = '{}_per_corpus_stats.csv'.format(elem_type)
    with open(fname, 'w', encoding='utf8') as f:
        writer = csv.writer(f)

        # Write the header.
        if elem_type == 'poses':
            writer.writerow(['corpus', elem_type, 'db1', 'db2', 'difference',
                             'in_manual'])
        else:
            writer.writerow(['corpus', elem_type, 'db1', 'db2', 'difference'])

        # Write data.
        for corpus in elem_stats:
            es_corp = elem_stats[corpus]
            for elem in es_corp:
                ec_stats = es_corp[elem]
                freq1 = ec_stats['db1']
                freq2 = ec_stats['db2']
                diff = ec_stats['diff']
                if elem_type == 'poses':
                    in_manual = ec_stats['in_manual']
                    write_pos_row(writer, corpus, elem, freq1, freq2, diff,
                                  in_manual)
                else:
                    write_elem_row(writer, corpus, elem, freq1, freq2, diff)


def write_elem_row(writer, corpus, elem, freq1, freq2, diff):
    if od:
        if diff != 0 and diff is not None:
            row = [corpus, elem, freq1, freq2, diff]
            writer.writerow(row)
    else:
        row = [corpus, elem, freq1, freq2, diff]
        writer.writerow(row)


def write_pos_row(writer, corpus, elem, freq1, freq2, diff, in_manual):
    if od:
        if diff != 0 and diff is not None:
            row = [corpus, elem, freq1, freq2, diff, in_manual]
            writer.writerow(row)
    else:
        row = [corpus, elem, freq1, freq2, diff, in_manual]
        writer.writerow(row)


def main():
    print('set up paths and load DBs...')
    setup()
    print('get common corpora...')
    common_corpora = get_common_corpora()
    stats = {}
    print('calculate global statistics...')
    stats['global'] = get_corpus_statistics(common_corpora)
    for corpus in common_corpora:
        print('calculate {} statistics...'.format(corpus))
        stats[corpus] = get_corpus_statistics([corpus])
    print('write to file')
    write_corpus_stats(stats)

    print('calculate word level statistics...')
    word_stats = get_word_stats(common_corpora)
    print('write to file')
    write_elem_stats(word_stats, 'words')

    print('calculate morpheme level statistics...')
    word_stats = get_morpheme_stats(common_corpora)
    print('write to file')
    write_elem_stats(word_stats, 'morphemes')

    print('calculate gloss level statistics...')
    word_stats = get_gloss_stats(common_corpora)
    print('write to file')
    write_elem_stats(word_stats, 'glosses')

    print('calculate pos level statistics...')
    word_stats = get_pos_stats(common_corpora)
    print('write to file')
    write_elem_stats(word_stats, 'poses')

    print('Done')


if __name__ == '__main__':
    main()
