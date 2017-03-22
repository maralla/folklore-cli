# -*- coding: utf-8 -*-

import pytest
from docopt import DocoptExit


def test_help_run():
    from takumi_cli.cmds.help import run
    cmd = run(['serve'])
    assert cmd == 'serve'


def test_validation():
    from takumi_cli.cmds.help import run

    with pytest.raises(DocoptExit) as e:
        run([])
    assert 'Usage' in str(e.value)
