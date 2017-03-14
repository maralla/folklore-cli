# -*- coding: utf-8 -*-

import mock
import sys


def test_create_client_pool(app_yaml):
    from takumi_cli.cmds.shell import _create_client_pool
    c = _create_client_pool('localhost')
    assert hasattr(c, 'ping')
    assert callable(c.ping)


def test_run(app_yaml, monkeypatch):
    from takumi_cli.cmds.shell import run, _ClientWrapper
    shell = mock.Mock()
    import IPython
    monkeypatch.setattr(IPython, 'start_ipython', shell)

    mock_pool = mock.Mock()
    mock_client = mock.Mock(_pool=mock_pool)
    monkeypatch.setattr(_ClientWrapper, '__new__',
                        mock.Mock(return_value=mock_client))

    run(['-t', 'www.example.com', '--', '-i', 'hello.py'])
    shell.assert_called_with(
        argv=['-i', 'hello.py'],
        user_ns={'c': mock_client},
        config={'TerminalInteractiveShell': {
            'banner1': """Python {}

Interactive shell for service test.
c         -> Client for invoking service api.
c._thrift -> Loaded thrift module.
""".format(sys.version.split('\n')[0].strip())
        }})
