# -*- coding: utf-8 -*-

"""Deploy a Takumi app.

Usage:
    takumi_deploy <target> [<ansible_args>...]
    takumi_deploy -h | --help | --help-ansible

Options:
    -h, --help      Show this message and exit
    --help-ansible  Show ansible help
"""

import schema
from docopt import docopt, DocoptExit

from ..deploy import start

validator = schema.Schema({
    '--help': bool,
    '--help-ansible': bool,
    '<target>': schema.Or(None, str),
    '<ansible_args>': list
})


def run(args):
    args = docopt(__doc__, argv=args, options_first=True)

    try:
        args = validator.validate(args)
    except schema.SchemaError as e:
        raise DocoptExit('{}\n'.format(e))

    if args['--help-ansible']:
        args['<ansible_args>'] = ['-h']

    try:
        start(args['<target>'], args['<ansible_args>'])
    except Exception as e:
        raise DocoptExit('{}\n'.format(e))
