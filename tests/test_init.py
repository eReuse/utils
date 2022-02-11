import json

from ereuse_utils import Dumpeable


def test_dumpeable():
    class Foo(Dumpeable):
        def __init__(self):
            self.foo = 1
            self._bar = 2
            self.foo_bar = '3'

    foo = Foo()
    f = json.loads(foo.to_json())
    assert f['foo'] == 1
    assert f['fooBar'] == '3'
    assert len(f) == 2
