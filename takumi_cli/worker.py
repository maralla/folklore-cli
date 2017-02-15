# -*- coding: utf-8 -*-

"""
takumi_cli.worker
~~~~~~~~~~~~~~~~~

This module implements a Takumi specific gevent worker. This is the only worker
Takumi supports.
"""

import socket
import errno

import gunicorn.workers
from gunicorn.workers.ggevent import GeventWorker

from thriftpy.transport import TSocket
from thriftpy.protocol.exc import TProtocolException
from thriftpy.protocol.cybin import ProtocolError
from thriftpy.transport import TTransportException

from takumi_service.service import Service


class Worker(GeventWorker):
    def handle(self, listener, client, addr):
        thrift_service = Service()
        ctx = thrift_service.context
        # clear context
        ctx.clear()
        ctx['client_addr'] = addr[0]
        ctx['worker'] = self

        client_timeout = self.app.cfg.client_timeout
        if client_timeout is not None:
            client.settimeout(client_timeout)

        handler_getter = self.app.wsgi()
        thrift_service.set_handler(handler_getter())
        sock = TSocket()
        sock.set_handle(client)
        try:
            thrift_service.run(sock)
        except TTransportException:
            pass
        except (TProtocolException, ProtocolError) as err:
            self.log.warning('Protocol error, is client(%s) correct? %s',
                             addr, err)
        except socket.timeout:
            self.log.warning('Client timeout: %r', addr)
        except socket.error as e:
            if e.args[0] == errno.ECONNRESET:
                self.log.debug('%r: %r', addr, e)
            elif e.args[0] == errno.EPIPE:
                self.log.warning('%r: %r', addr, e)
            else:
                self.log.exception('%r: %r', addr, e)
        except Exception as e:
            self.log.exception('%r: %r', addr, e)
        finally:
            ctx.clear()

# Replace gunicorn default workers
gunicorn.workers.SUPPORTED_WORKERS.clear()
gunicorn.workers.SUPPORTED_WORKERS[
    'gevent_thriftpy'] = 'takumi_cli.worker.Worker'
