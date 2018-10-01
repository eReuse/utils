from unittest import mock

import ereuse_utils


def test_if_none_return_none():
    mocked = mock.MagicMock()
    wrapped = ereuse_utils.if_none_return_none(mocked)
    assert mocked.call_count == 0
    wrapped(None, 3)
    assert mocked.call_count == 1
    assert mocked.call_args == mock.call(None, 3)
    wrapped(None, None)
    assert mocked.call_count == 1
