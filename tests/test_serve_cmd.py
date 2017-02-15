# -*- coding: utf-8 -*-

import mock


def test_serve_run(app_yaml, gunicorn_serve):
    from takumi_cli.app import AppRunner
    from takumi_cli.cmds.serve import run

    with mock.patch.object(AppRunner, 'run') as mock_run:
        run([])
    mock_run.assert_called_with()
