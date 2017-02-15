# -*- coding: utf-8 -*-

"""Serve a takumi thrift service.

Usage:
    takumi serve [<gunicorn_args>...]
"""

import sys

from ..app import AppRunner


def run(args):
    # Replace argv
    sys.argv = ['takumi serve'] + args
    # Delegate to gunicorn
    AppRunner().run()
