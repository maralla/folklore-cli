# -*- coding: utf-8 -*-

import pytest
import mock
import sys
from docopt import DocoptExit
import folklore_cli.cmds as cmds


@pytest.fixture
def cmd():
    c = []
    with mock.patch.object(sys, 'argv', c):
        yield c


def test_validation(cmd):
    cmd.extend(['folklore', 'missing'])
    with pytest.raises(DocoptExit) as e:
        cmds.main()
    assert ("`<command>` should be one of "
            "('help', 'run', 'test', 'serve', "
            "'deploy', 'shell')") in str(e.value)


def test_help(cmd, monkeypatch):
    import folklore_cli.cmds.serve
    mock_serve = mock.Mock()
    monkeypatch.setattr(folklore_cli.cmds.serve, 'run', mock_serve)

    cmd[:] = ['folklore', 'help', 'serve']
    cmds.main()
    mock_serve.assert_called_with(['-h'])


def test_serve(cmd, monkeypatch):
    import folklore_cli.cmds.serve
    mock_serve = mock.Mock()
    monkeypatch.setattr(folklore_cli.cmds.serve, 'run', mock_serve)

    cmd[:] = ['folklore', 'serve']
    cmds.main()
    mock_serve.assert_called_with([])


def test_deploy(cmd, monkeypatch):
    import folklore_cli.cmds.deploy
    mock_deploy = mock.Mock()
    monkeypatch.setattr(folklore_cli.cmds.deploy, 'run', mock_deploy)

    cmd[:] = ['folklore', 'deploy', 'testing']
    cmds.main()
    mock_deploy.assert_called_with(['testing'])


def test_shell(cmd, monkeypatch):
    import folklore_cli.cmds.shell
    mock_shell = mock.Mock()
    monkeypatch.setattr(folklore_cli.cmds.shell, 'run', mock_shell)

    cmd[:] = ['folklore', 'shell', '--', '-i', 'hello.py']
    cmds.main()
    mock_shell.assert_called_with(['--', '-i', 'hello.py'])
