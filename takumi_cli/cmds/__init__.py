# -*- coding: utf-8 -*-

"""Takumi command line toolkit.

Usage:
    takumi <command> [<args>...]
    takumi -h | --help

Options:
    -h, --help      Show this message and exit
    --version       Show version

Commands:
    help            Show help for command
    run             Run script
    test            Run tests
    serve           Serve the service using gunicorn
    deploy          Deploy the service to an environment
    shell           Start an IPython REPL
"""

import schema
from docopt import docopt

from .help import run as run_help
from .serve import run as run_serve
from .deploy import run as run_deploy

__version__ = '0.1.0'

commands = 'help', 'run', 'test', 'serve', 'deploy', 'shell'


validator = schema.Schema({
    '<command>': schema.And(
        str, lambda c: c in commands,
        error='`<command>` should be one of {}'.format(commands)),
    '<args>': list,
    '--help': bool,
})


def run(command, args):
    if command == 'help':
        cmd = run_help(args)
        run(cmd, ['-h'])
    elif command == 'serve':
        run_serve(args)
    elif command == 'deploy':
        run_deploy(args)
    else:
        exit('Command {!r} not supported'.format(command))


def main():
    args = docopt(__doc__, version=__version__, options_first=True)
    try:
        args = validator.validate(args)
    except schema.SchemaError as e:
        exit(e)

    run(args['<command>'], args['<args>'])
