import subprocess
from unittest import mock

import pytest

from ereuse_utils import cmd


def test_cmd_run_normal():
    out = cmd.run('echo', '1').stdout.strip()
    assert out == '1'


def test_cmd_run_shell():
    out = cmd.run('echo', '1', shell=True).stdout.strip()
    assert out == '1'


@pytest.fixture()
def mock_popen():
    subprocess.Popen = mock.MagicMock()


@pytest.mark.usefixtures('mock_popen')
def test_progressive_cmd_read_line_int():
    """Tests Progressive CMD with a command that reads lines
    and the percentage is formatted as naturals, like shred.
    """
    p = cmd.ProgressiveCmd('foo', callback=mock.MagicMock(), check=False)
    p.out = mock.MagicMock()
    p.out.readline = mock.MagicMock()
    p.out.readline.side_effect = ['shred: /dev/sda: pass 1/1 (random)...', None]
    p.run()
    assert p._callback.call_count == 0, 'Progressive CMD does not update when completed'

    p = cmd.ProgressiveCmd('foo', callback=mock.MagicMock(), check=False)
    p.out = mock.MagicMock()
    p.out.readline = mock.MagicMock()
    t = 'shred: /dev/sda: pass 1/1 (random)...111MiB/5.0GiB {}%'
    p.out.readline.side_effect = [t.format(1), t.format(20), t.format(100), None]
    p.run()
    # first increment is 5, which is 20 / 4
    # second increment is 20, which is 100 / 4 - 5
    assert p._callback.call_args_list == [mock.call(1, 1), mock.call(19, 20), mock.call(80, 100)]


@pytest.mark.usefixtures('mock_popen')
def test_progressive_cmd_read_chars_decimal():
    """Tests progressive CMD with a command that does not print lines
    and the percentage is formatted as decimals, like badblocks.
    """
    t = 'Reading and comparing: {}% done, 0:50 elapsed. (0/0/0 errors)'
    p = cmd.ProgressiveCmd('foo',
                           number_chars=cmd.ProgressiveCmd.DECIMALS,
                           decimal_numbers=cmd.ProgressiveCmd.DECIMAL_NUMBERS,
                           read=10,
                           callback=mock.MagicMock(),
                           check=False)
    p.out = mock.MagicMock()
    p.out.read = mock.MagicMock()

    p.out.read.side_effect = [t.format('20.44'), t.format('90.00'), t.format('30.00'),
                              t.format('80.01'), t.format('100.01'), None]
    p.run()
    # Note that for 30.00 we don't have any increment (as it would be negative)
    # so the software doesn't perform to _callback on that one
    assert p._callback.call_args_list == [
        mock.call(20.44, 20.44),
        mock.call(69.56, 90.0),
        mock.call(50.010000000000005, 80.01),
        mock.call(20, 100.01)
    ]

    p = cmd.ProgressiveCmd('foo',
                           number_chars=cmd.ProgressiveCmd.DECIMALS,
                           read=10,
                           callback=mock.MagicMock(),
                           check=False)
    p.out = mock.MagicMock()
    p.out.read = mock.MagicMock()

    p.out.read.side_effect = ['Testing with random pattern: done', None]
    p.run()
    assert p._callback.call_count == 0
