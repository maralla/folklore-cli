# -*- coding: utf-8 -*-

"""Serve a takumi thrift service.

Usage:
    takumi_serve [<gunicorn_args>...]
"""


def run(args):
    from ..runner import AppRunner
    # Delegate to gunicorn
    AppRunner().run()
