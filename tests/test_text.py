import math

from ereuse_utils.text import numbers, positive_percentages, macs


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
    assert not len(tuple(positive_percentages('45')))
    assert not len(tuple(positive_percentages('')))


def test_macs():
    assert '13:bc:16:ff:45:34' == next(macs('foo 13:bc:16:ff:45:34 bar'))
