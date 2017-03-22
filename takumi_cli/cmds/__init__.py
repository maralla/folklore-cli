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

import sys
import schema
from docopt import docopt, DocoptExit

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
        from .help import run as help
        cmd = help(args)
        return run(cmd, ['-h'])
    if command == 'serve':
        from .serve import run as serve
        return serve(args)
    if command == 'deploy':
        from .deploy import run as deploy
        return deploy(args)
    if command == 'shell':
        from .shell import run as shell
        return shell(args)
    raise DocoptExit('Command {!r} not supported\n'.format(command))


def main():
    args = docopt(__doc__, version=__version__, options_first=True)
    try:
        args = validator.validate(args)
    except schema.SchemaError as e:
        raise DocoptExit('{}\n'.format(e))

    # replace argv
    sys.argv = [' '.join(sys.argv[:2])] + sys.argv[2:]
    run(args['<command>'], args['<args>'])
