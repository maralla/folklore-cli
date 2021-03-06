# -*- coding: utf-8 -*-


def test_set_cfg(app_yaml, gunicorn_serve):
    from folklore_cli.runner import AppRunner, Worker

    app = AppRunner()
    app.init(None, None, None)

    assert app.cfg.default_proc_name == 'test'
    assert app.cfg.worker_class is Worker
    assert app.cfg.worker_connections == 10
    assert app.cfg.loglevel == 'info'
    assert app.cfg.graceful_timeout == 3
    assert app.cfg.timeout == 30
    assert app.cfg.bind == ['0.0.0.0:8010']
    assert app.cfg.workers == 2
    assert app.cfg.errorlog == '-'
    assert app.cfg.client_timeout == 1200


def test_load_app(app_yaml, gunicorn_serve):
    from folklore_cli.runner import AppRunner
    import app as mock_app

    app = AppRunner()
    getter = app.load()
    handler = getter()
    assert handler == mock_app.app
