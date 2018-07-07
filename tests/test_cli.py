import pathlib
from enum import Enum

import click
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
