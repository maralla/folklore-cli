# -*- coding: utf-8 -*-

import mock


def test_serve_run(app_yaml, gunicorn_serve):
    from folklore_cli.runner import AppRunner
    from folklore_cli.cmds.serve import run

    with mock.patch.object(AppRunner, 'run') as mock_run:
        run([])
    mock_run.assert_called_with()
