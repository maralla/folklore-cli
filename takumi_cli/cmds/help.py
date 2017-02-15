# -*- coding: utf-8 -*-

"""Show help for specific command.

Usage:
    takumi help <command>
    takumi help -h | --help

Options:
    -h, --help      Show this message and exit
"""

import schema
from docopt import docopt

validator = schema.Schema({
    '<command>': str,
    '--help': bool,
    'help': bool
})


def run(args):
    argv = ['help'] + args
    args = docopt(__doc__, argv=argv)

    try:
        args = validator.validate(args)
    except schema.SchemaError as e:
        exit(e)

    return args['<command>']
