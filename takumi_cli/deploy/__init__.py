# -*- coding: utf-8 -*-

"""
takumi_cli.deploy
~~~~~~~~~~~~~~~~~

Implement deploy command using ansible.
"""

import os

PLAYBOOK_PATH = os.path.join(
    os.path.dirname(__file__), 'playbook', 'playbook.yml')


def _find_hosts(cwd):
    hosts = os.path.join(cwd, 'hosts')
    if os.path.isfile(hosts):
        return hosts


def _compose_args(target, args):
    if '--limit' not in args:
        args.extend(['--limit', target])
    args.append(PLAYBOOK_PATH)
    cwd = os.getcwd()
    hosts = _find_hosts(cwd)
    if hosts and '-i' not in args and '--inventory-file' not in args:
        args.extend(['-i', hosts])
    args.extend(['-e', 'app_repo={}'.format(cwd)])
    return ['ansible-playbook'] + args


def start(target, args):
    """Start deployment powered by ansible.

    :param target: hosts to deploy
    :param args: arguments passed to ansible
    """
    ansible_args = _compose_args(target, args)
    from ansible.cli.playbook import PlaybookCLI
    cli = PlaybookCLI(ansible_args)
    cli.parse()
    cli.run()
