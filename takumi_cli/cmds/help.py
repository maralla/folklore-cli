# -*- coding: utf-8 -*-

"""Show help for specific command.

Usage:
    takumi_help <command>
    takumi_help -h | --help

Options:
    -h, --help      Show this message and exit
"""

import schema
from docopt import docopt

validator = schema.Schema({
    '<command>': str,
    '--help': bool,
})


def run(args):
    args = docopt(__doc__, argv=args)

    try:
        args = validator.validate(args)
    except schema.SchemaError as e:
        exit(e)

    return args['<command>']
