# -*- coding: utf-8 -*-

import mock
import socket
import logging
import errno


class MockContext(dict):
    clear = mock.Mock()


class MockService(object):
    context = MockContext()
    run = mock.Mock()
    set_handler = mock.Mock()


def test_worker_handle(app_yaml, gunicorn_serve, monkeypatch):
    import takumi_service.service as takumi_service_
    from takumi_cli.runner import AppRunner, Worker
    from .app import app as mock_app

    logger = logging.getLogger('test')

    app = AppRunner()
    worker = Worker(age=1, ppid=1, sockets=[], app=app,
                    timeout=30, cfg=app.cfg, log=logger)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    mock_service = mock.Mock(return_value=MockService)
    monkeypatch.setattr(takumi_service_, 'TakumiService', mock_service)

    worker.handle(None, sock, ('127.0.0.1', 8465))
    assert MockService.context['client_addr'] == '127.0.0.1'
    assert isinstance(MockService.context['worker'], Worker)
    assert MockService.context['worker'].alive
    MockService.run.assert_called()
    MockService.set_handler.assert_called_with(mock_app)

    logger.warn = mock.Mock()
    MockService.run.side_effect = socket.timeout('hello')
    worker.handle(None, sock, ('127.0.0.1', 8465))
    logger.warn.assert_called_with('Client timeout: %r', ('127.0.0.1', 8465))

    logger.debug = mock.Mock()
    MockService.run.side_effect = socket.error(errno.ECONNRESET)
    worker.handle(None, sock, ('127.0.0.1', 8465))
    logger.debug.assert_called_with('%r: %s', ('127.0.0.1', 8465),
                                    str(errno.ECONNRESET))

    MockService.run.side_effect = socket.error(errno.EPIPE)
    worker.handle(None, sock, ('127.0.0.1', 8465))
    logger.warn.assert_called_with('%r: %s', ('127.0.0.1', 8465),
                                   str(errno.EPIPE))

    logger.exception = mock.Mock()
    MockService.run.side_effect = socket.error(errno.E2BIG)
    worker.handle(None, sock, ('127.0.0.1', 8465))
    logger.exception.assert_called_with('%r: %s', ('127.0.0.1', 8465),
                                        str(errno.E2BIG))

    MockService.run.side_effect = TypeError
    worker.handle(None, sock, ('127.0.0.1', 8465))
    logger.exception.assert_called_with('%r: %s', ('127.0.0.1', 8465), '')
