# -*- coding: utf-8 -*-

import mock
import socket
from gunicorn.sock import create_sockets
import takumi_cli.worker as takumi_cli_worker
from takumi_cli.worker import Worker


class MockContext(dict):
    clear = mock.Mock()


class MockService(object):
    context = MockContext()
    run = mock.Mock()
    set_handler = mock.Mock()


def test_worker_handle(app_yaml, gunicorn_serve):
    from takumi_cli.app import AppRunner
    from .app import app as mock_app

    app = AppRunner()
    socks = create_sockets(app.cfg, None)
    worker = Worker(age=1, ppid=1, sockets=socks, app=app,
                    timeout=30, cfg=app.cfg, log=None)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with mock.patch.object(takumi_cli_worker, 'Service',
                           return_value=MockService):
        worker.handle(worker.sockets[0], sock, ('127.0.0.1', 8465))

    assert MockService.context['client_addr'] == '127.0.0.1'
    assert isinstance(MockService.context['worker'], Worker)
    assert MockService.context['worker'].alive
    MockService.run.assert_called()
    MockService.set_handler.assert_called_with(mock_app)
