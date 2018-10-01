import pathlib
from enum import Enum

import click
from boltons import urlutils
from click.testing import CliRunner

from ereuse_utils import cli


def test_cli_enum():
    class FooEnum(Enum):
        Foo = 1
        Bar = 2

    @click.command()
    @click.option('--foo', type=cli.Enum(FooEnum))
    def foo(foo: FooEnum):
        print(foo.value)

    runner = CliRunner()
    result = runner.invoke(foo, ('--foo', 'Bar'))
    assert result.exit_code == 0
    assert result.output.strip() == '2'


def test_cli_path():
    @click.command()
    @click.option('--foo', type=cli.Path())
    def foo(foo: pathlib.Path):
        assert isinstance(foo, pathlib.Path)
        print(foo)

    runner = CliRunner()
    result = runner.invoke(foo, ('--foo', '/foo/bar'))
    assert result.exit_code == 0
    assert result.output.strip() == '/foo/bar'


def test_url():
    @click.command()
    @click.option('--foo', type=cli.URL())
    def foo(foo: urlutils.URL):
        assert isinstance(foo, urlutils.URL)
        print(foo.to_text())

    runner = CliRunner()
    result = runner.invoke(foo, ('--foo', 'https://www.foo.bar'))
    assert result.exit_code == 0
    assert result.output.strip() == 'https://www.foo.bar'

    @click.command()
    @click.option('--foo', type=cli.URL(scheme=True, username=True, password=False))
    def foo(foo: urlutils.URL):
        assert isinstance(foo, urlutils.URL)
        print(foo.to_text())

    result = runner.invoke(foo, ('--foo', 'https://www.foo.bar'))
    assert result.exit_code == 2
    result = runner.invoke(foo, ('--foo', 'https://foo@foo.bar'))
    assert result.exit_code == 0
    assert result.output.strip() == 'https://foo@foo.bar'
    result = runner.invoke(foo, ('--foo', 'https://foo:bar@foo.bar'))
    assert result.exit_code == 2
    assert 'cannot contain password but it does' in result.output

    @click.command()
    @click.option('--foo', type=cli.URL(scheme=True, username='foo', password=False))
    def foo(foo: urlutils.URL):
        assert isinstance(foo, urlutils.URL)
        print(foo.to_text())

    result = runner.invoke(foo, ('--foo', 'https://foo@foo.bar'))
    assert result.exit_code == 0
    result = runner.invoke(foo, ('--foo', 'https://bar@foo.bar'))
    assert result.exit_code == 2
