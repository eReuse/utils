from ereuse_utils import cmd


def test_cmd_run():
    out = cmd.run('echo', '1').stdout.strip()
    assert out == '1'
