import subprocess
from unittest import mock

import pytest

from ereuse_utils import cmd


def test_cmd_run():
    out = cmd.run('echo', '1').stdout.strip()
    assert out == '1'


@pytest.fixture()
def mock_popen():
    subprocess.Popen = mock.MagicMock()


@pytest.mark.usefixtures('mock_popen')
def test_progressive_cmd_read_line_int():
    """Tests Progressive CMD with a command that reads lines
    and the percentage is formatted as naturals, like shred.
    """
    p = cmd.ProgressiveCmd('foo', callback=mock.MagicMock())
    p.out = mock.MagicMock()
    p.out.readline = mock.MagicMock()
    p.out.readline.side_effect = ['shred: /dev/sda: pass 1/1 (random)...', None]
    p.run()
    assert p._callback.call_count == 1, 'Progressive CMD updates only 1 when completed'

    p = cmd.ProgressiveCmd('foo', callback=mock.MagicMock())
    p.out = mock.MagicMock()
    p.out.readline = mock.MagicMock()
    t = 'shred: /dev/sda: pass 1/1 (random)...111MiB/5.0GiB {}%'
    p.out.readline.side_effect = [t.format(20), t.format(100), None]
    p.run()
    # first increment is 5, which is 20 / 4
    # second increment is 20, which is 100 / 4 - 5
    assert p._callback.call_args_list == [mock.call(20), mock.call(80), mock.call(0)]


@pytest.mark.usefixtures('mock_popen')
def test_progressive_cmd_read_chars_decimal():
    """Tests progressive CMD with a command that does not print lines
    and the percentage is formatted as decimals, like badblocks.
    """
    t = 'Reading and comparing: {}% done, 0:50 elapsed. (0/0/0 errors)'
    p = cmd.ProgressiveCmd('foo',
                           number_chars=cmd.ProgressiveCmd.DECIMALS,
                           read=10,
                           callback=mock.MagicMock())
    p.out = mock.MagicMock()
    p.out.read = mock.MagicMock()

    p.out.read.side_effect = [t.format(20.44), t.format(90.00), t.format(30.00), t.format(80.01),
                              None]
    p.run()
    assert p._callback.call_args_list == [mock.call(20), mock.call(70), mock.call(0),
                                          mock.call(50), mock.call(20)]

    p = cmd.ProgressiveCmd('foo',
                           number_chars=cmd.ProgressiveCmd.DECIMALS,
                           read=10,
                           callback=mock.MagicMock())
    p.out = mock.MagicMock()
    p.out.read = mock.MagicMock()

    p.out.read.side_effect = ['Testing with random pattern: done', None]
    p.run()
    assert p._callback.call_count == 1
