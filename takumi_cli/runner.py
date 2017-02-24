# -*- coding: utf-8 -

"""
takumi_cli.runner
~~~~~~~~~~~~~~~~~

This module implements the `serve` command. This command is used for running
Takumi services using gunicorn gevent worker.

Available hooks:

    - after_load    Hook to be called after app imported

Registered hooks:

    - after_load    config_log
"""

import errno
import os
import socket
import sys

import gunicorn.workers

from gunicorn.app.base import Application
from gunicorn.config import Setting, validate_pos_int
from gunicorn.util import import_app
from gunicorn.workers.ggevent import GeventWorker

from thriftpy.protocol.cybin import ProtocolError
from thriftpy.protocol.exc import TProtocolException
from thriftpy.transport import TSocket
from thriftpy.transport import TTransportException

from takumi_config import config
from takumi_service.hook import hook_registry
from takumi_service.log import config_log
from takumi_service.service import TakumiService

# register log config hook
hook_registry.register(config_log)


class Worker(GeventWorker):
    def handle(self, listener, client, addr):
        thrift_service = TakumiService()
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
    'gevent_thriftpy'] = 'takumi_cli.runner.Worker'


class ClientTimeout(Setting):
    name = "client_timeout"
    cli = ["--client-timeout"]
    validator = validate_pos_int
    default = None
    desc = """\
        Seconds to timeout a client if client is silent after this duration
    """


class AppRunner(Application):
    def chdir(self):
        # chdir to the configured path before loading,
        # default is the current dir
        os.chdir(self.cfg.chdir)

        # add the path to sys.path
        sys.path.insert(0, self.cfg.chdir)

    def load(self):
        self.chdir()

        def load_app():
            app = import_app(config.app)
            hook_registry.on_after_load()
            return app
        return load_app

    def set_cfg(self):
        self.cfg.set('default_proc_name', config.app_name)
        self.cfg.set('worker_class', config.worker_class)
        self.cfg.set('worker_connections', config.worker_connections)
        self.cfg.set('loglevel', 'info')
        self.cfg.set('graceful_timeout', 3)
        self.cfg.set('timeout', config.timeout)
        self.cfg.set('bind', '0.0.0.0:{}'.format(config.port))
        self.cfg.set('workers', config.workers)

        if config.env.name is 'dev' or config.syslog_disabled:
            self.cfg.set('errorlog', '-')
        else:
            self.cfg.set('syslog', True)
            self.cfg.set('syslog_facility', 'local6')
            self.cfg.set('syslog_addr', 'unix:///dev/log#dgram')

    def init(self, parser, opts, args):
        self.set_cfg()
        self.cfg.set('client_timeout', config.client_timeout)
        self.patch_gunicorn()

    def patch_gunicorn(self):
        import gunicorn.sock

        def _tcp_socket_str(self):
            return 'tcp://%s:%d' % self.sock.getsockname()
        gunicorn.sock.TCPSocket.__str__ = _tcp_socket_str
