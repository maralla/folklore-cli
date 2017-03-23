# -*- coding: utf-8 -*-

"""Deploy a Takumi app.

Usage:
    takumi_deploy <target> [options] [(-- <ansible_args>...)]
    takumi_deploy -- <ansible_args>...
    takumi_deploy -h | --help

Options:
    -t, --tags TAGS  Only run tasks with these tags
    -p, --play PLAY  Specify a different playbook
    -h, --help       Show this message and exit

Example:

    Simple deploy:

        takumi deploy testing

    Deploy a subject:

        takumi deploy testing -t cron

    Specify other playbooks:

        takumi deploy testing -p system.yml
"""

import schema
from docopt import docopt, DocoptExit

validator = schema.Schema({
    '--tags': schema.Or(None, str),
    '--play': schema.Or(None, str),
    '<target>': schema.Or(None, lambda x: x != '--',
                          error='Invalid value of target'),
    '<ansible_args>': schema.Or(None, list)
}, ignore_extra_keys=True)


def run(args):
    args = docopt(__doc__, argv=args)
    try:
        args = validator.validate(args)
    except schema.SchemaError as e:
        raise DocoptExit('{}\n'.format(e))

    from ..deploy import start

    try:
        start(args)
    except Exception as e:
        exit('Fail to deploy: {}'.format(e))
