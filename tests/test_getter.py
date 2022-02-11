from ereuse_utils import getter as g


def test_getter():
    assert g.dict({'foo': '53'}, 'foo') == 53
    assert g.dict({'foo': {'bar': '42'}}, ('foo', 'bar'), type=str) == '42'
    assert g.kv(['x:4'], 'x') == 4
    assert next(g.indents(['foo1', '  bar', ''], 'fo')) == ['foo1', '  bar']


def test_sanitize_parenthesis():
    """Parenthesis, square brackets..."""
    assert g.sanitize('Foo (NONE)') == 'Foo'
    assert g.sanitize('Foo (none)') == 'Foo'
    assert g.sanitize('foo(O.E.M)') == 'foo'
    assert g.sanitize('foo(o.e.m)') == 'foo'
    assert g.sanitize('foo(o.e.M)') == 'foo'
    assert g.sanitize('System[[n/a]') == 'System'
    assert g.sanitize('system[[n/a]') == 'system'
    assert g.sanitize('system serial[[n/a]') is None
    assert g.sanitize('system SERIAL[[n/a]') is None
    assert g.sanitize('systemserial[[n/a]') == 'systemserial'


def test_sanitize_none():
    assert g.sanitize('none') is None
    assert g.sanitize('NONE') is None
    assert g.sanitize('none foo') == 'foo'


def test_sanitize_unknown():
    assert g.sanitize('Unknown') is None
    assert g.sanitize('unknown') is None


def test_sanitize_remove():
    assert g.sanitize('foobar', remove={'foobar'}) is None
    assert g.sanitize('foobarx', remove={'foobar'}) == 'foobarx'


def test_sanitize_cpu_values():
    # Note that we still remove the S/N of cpus in computer.processors()
    assert g.sanitize('0001-067A-0000-0000-0000-0000') is None
    assert g.sanitize('0001-067A-0000-0000') is None
