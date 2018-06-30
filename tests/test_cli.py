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
        return print(foo.value)

    runner = CliRunner()
    result = runner.invoke(foo, ('--foo', 'Bar'))
    assert result.exit_code == 0
    assert result.output.strip() == '2'
