# -*- coding: utf-8 -*-

"""Serve a takumi thrift service.

Usage:
    takumi_serve [<gunicorn_args>...]
"""

from ..app import AppRunner


def run(args):
    # Delegate to gunicorn
    AppRunner().run()
