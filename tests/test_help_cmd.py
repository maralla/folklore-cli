# -*- coding: utf-8 -*-


def test_help_run():
    from takumi_cli.cmds.help import run
    cmd = run(['serve'])
    assert cmd == 'serve'
