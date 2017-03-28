""" Regression tests for test acqdiv database. """

import pandas as pd
import numpy.testing as npt

import sqlite3
from nose.tools import assert_true

# Set up
test_db = sqlite3.connect("../database/test.sqlite3")
gold_db = sqlite3.connect("fixtures/gold.sqlite3")


def test_sessions():
    test = pd.read_sql_query("SELECT * from sessions", test_db)
    gold = pd.read_sql_query("SELECT * from sessions", gold_db)
    assert_true(test.equals(gold))
    if not assert_true(test.equals(gold)):
        assert_frames_equal(test, gold)


def test_utterances():
    test = pd.read_sql_query("SELECT * from utterances", test_db)
    gold = pd.read_sql_query("SELECT * from utterances", gold_db)
    if not test.equals(gold):
        assert_frames_equal(test, gold)
    assert_true(test.equals(gold))


def test_speakers():
    test = pd.read_sql_query("SELECT * from speakers", test_db)
    gold = pd.read_sql_query("SELECT * from speakers", gold_db)
    if not test.equals(gold):
        assert_frames_equal(test, gold)
    assert_true(test.equals(gold))


def test_uniquespeakers():
    test = pd.read_sql_query("SELECT * from uniquespeakers", test_db)
    gold = pd.read_sql_query("SELECT * from uniquespeakers", gold_db)
    if not test.equals(gold):
        assert_frames_equal(test, gold)
    assert_true(test.equals(gold))


def test_words():
    test = pd.read_sql_query("SELECT * from words", test_db)
    gold = pd.read_sql_query("SELECT * from words", gold_db)
    if not test.equals(gold):
        assert_frames_equal(test, gold)
    assert_true(test.equals(gold))


def test_morphemes():
    test = pd.read_sql_query("SELECT * from morphemes", test_db)
    gold = pd.read_sql_query("SELECT * from morphemes", gold_db)
    if not test.equals(gold):
        assert_frames_equal(test, gold)
    assert_true(test.equals(gold))


def assert_frames_equal(actual, expected, use_close=False):
    """
    Compare DataFrame items by index and column and
    raise AssertionError if any item is not equal.

    Ordering is unimportant, items are compared only by label.
    NaN and infinite values are supported.

    Parameters
    ----------
    actual : pandas.DataFrame
    expected : pandas.DataFrame
    use_close : bool, optional
        If True, use numpy.testing.assert_allclose instead of
        numpy.testing.assert_equal.

    Notes
    -----
    From code: https://gist.github.com/jiffyclub/ac2e7506428d5e1d587b
    actual = pd.DataFrame([[4, 1],[6, 3],[5, np.nan]],index=['x', 'z', 'y'],columns=['b', 'a'])
    expected = pd.DataFrame({'a': [1, np.nan, 3],'b': [np.nan, 5, 6]},index=['x', 'y', 'z'])
    assert_frames_equal(actual, actual)
    assert_frames_equal(actual, expected)
    """

    if use_close:
        comp = npt.assert_allclose
    else:
        comp = npt.assert_equal

    assert (isinstance(actual, pd.DataFrame) and
            isinstance(expected, pd.DataFrame)), \
        'Inputs must both be pandas DataFrames.'

    for i, exp_row in expected.iterrows():
        assert i in actual.index, 'Expected row {!r} not found.'.format(i)

        act_row = actual.loc[i]

        for j, exp_item in exp_row.iteritems():
            assert j in act_row.index, \
                'Expected column {!r} not found.'.format(j)

            act_item = act_row[j]

            try:
                comp(act_item, exp_item)
            except AssertionError as e:
                # raise AssertionError('\n\nColumn: {!r}\nRow: {!r}'.format(j, i))
                raise AssertionError('\n\nColumn: %s \nRow: %s' % (str(i), str(j)))
