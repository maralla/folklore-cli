# -*- coding: utf-8 -*-

"""Deploy a Takumi app.

Usage:
    takumi_deploy <target> [<ansible_args>...]
    takumi_deploy -h | --help

Options:
    -h, --help      Show this message and exit
"""

import schema
from docopt import docopt, DocoptExit

from ..deploy import start

validator = schema.Schema({
    '--help': bool,
    '<target>': str,
    '<ansible_args>': list
})


def run(args):
    args = docopt(__doc__, argv=args, options_first=True)

    try:
        args = validator.validate(args)
    except schema.SchemaError as e:
        raise DocoptExit('{}\n'.format(e))

    target = args['<target>']
    if target.startswith('-'):
        raise DocoptExit('Missing target\n')

    try:
        start(target, args['<ansible_args>'])
    except Exception as e:
        raise DocoptExit('{}\n'.format(e))
