import math

from ereuse_utils.text import clean, grep, macs, numbers, positive_percentages


def test_numbers():
    assert (315.0, 318.0) == tuple(numbers('315.0 x 318.0 dpi'))
    assert (315, 318) == tuple(numbers('315.0 x 318.0 dpi'))
    assert math.isclose(60.0, tuple(numbers('60.000004 fps'))[0], abs_tol=0.01)
    assert (720, 1280) == tuple(numbers('720 x 1280'))
    assert 16666666 == next(numbers('bufferDeadline 16666666'))
    assert -13.4 == next(numbers('foobar -13.4 xx'))
    assert 45 == next(numbers('45% completed'))
    assert 45.43 == next(numbers('completed 45.43%'))
    assert 4e9 == next(numbers('4e9'))


def test_positive_percentages():
    assert 45 == next(positive_percentages('45% completed'))
    assert 45.43 == next(positive_percentages('completed 45.43%'))
    assert 2 == next(positive_percentages('completed 2%'))
    assert 2 == next(positive_percentages('completed 02%'))
    assert 0.2 == next(positive_percentages('completed 00.2%'))
    assert 100 == next(positive_percentages('completed 100.00%'))
    assert not tuple(positive_percentages('45'))
    assert not tuple(positive_percentages(''))


def test_positive_percentages_num_chars():
    assert not tuple(positive_percentages('45% completed', {5}))
    assert 45.44 == next(positive_percentages('45.44% completed', {5}))
    assert 4 == next(positive_percentages('foo 04% completed', {2}))
    assert 90 == next(positive_percentages('foo 90.00% completed', {5}))
    assert 100 == next(positive_percentages('foo 100.00% completed', {6, 5}))
    assert 90 == next(positive_percentages('foo 90.00% completed', {6, 5}))
    assert not tuple(positive_percentages(''))


def test_positive_percentages_decimal_numbers():
    assert 45.44 == next(positive_percentages('45.44%', {5}, 2))
    assert 5.445 == next(positive_percentages('5.445%', {5}, 3))
    assert not tuple(positive_percentages('5.44%', {4}, 3))
    assert not tuple(positive_percentages('53.44%', {5}, 3))


def test_macs():
    assert '13:bc:16:ff:45:34' == next(macs('foo 13:bc:16:ff:45:34 bar'))


def test_grep():
    assert 'foo bar' == next(grep('oh\nfoo bar\n faz', 'bar'))
    assert ' faz' == next(grep('oh\nfoo bar \n faz', 'faz'))
    assert not tuple(grep('oh\nfoo bar \n faz', 'nope'))


def test_clean():
    assert clean('  foo foo \n\n foo \n\n') == 'foo foo foo'
