import json
from datetime import datetime

from ereuse_utils import JSONEncoder


def test_json_encoder():
    x = json.dumps({'foo': datetime(year=1984, month=1, day=1)}, cls=JSONEncoder)
    assert x == '{"foo": "1984-01-01T00:00:00"}'