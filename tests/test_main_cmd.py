# -*- coding: utf-8 -*-

import mock
import sys


def test_main(monkeypatch):
    import takumi_cli.cmds as cmds

    mock_help = mock.Mock(return_value='serve')
    mock_serve = mock.Mock()

    monkeypatch.setattr(cmds, 'run_help', mock_help)
    monkeypatch.setattr(cmds, 'run_serve', mock_serve)

    with mock.patch.object(sys, 'argv', ['takumi', 'help', 'serve']):
        cmds.main()
    mock_help.assert_called_with(['serve'])
    mock_serve.assert_called_with(['-h'])
