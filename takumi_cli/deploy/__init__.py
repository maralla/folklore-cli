# -*- coding: utf-8 -*-

"""
takumi_cli.deploy
~~~~~~~~~~~~~~~~~

Implement deploy command using ansible.
"""

import os
import tempfile
import json
from takumi_config import config

PLAYBOOK_PATH = os.path.join(
    os.path.dirname(__file__), 'playbook', 'playbook.yml')


def _find_hosts(cwd):
    hosts = os.path.join(cwd, 'hosts')
    if os.path.exists(hosts):
        return hosts


def _convert_hosts(hosts):
    ret = {}
    for k, v in hosts.items():
        converted = {}
        if not isinstance(v, dict):
            v = {'hosts': v}
        hs = v.get('hosts', [])
        if isinstance(hs, str):
            hs = [hs]
        for item in hs:
            if not isinstance(item, dict):
                item = {item: None}
            converted.update(item)
        v['hosts'] = converted
        ret[k] = v
    return ret


def _gen_hosts(deploy_config):
    hosts = deploy_config.get('targets', {})
    hosts = _convert_hosts(hosts)

    deploy_vars = deploy_config.get('vars', {})
    deploy_vars['app_name'] = config.app_name
    entry = {
        'service-deploy': {
            'vars': deploy_vars,
            'children': hosts
        }
    }
    hosts_file = tempfile.mktemp()
    with open(hosts_file, 'w') as f:
        f.write(json.dumps(entry))
    return hosts_file


def _compose_args(target, args):
    if '--limit' not in args:
        args.extend(['--limit', target])
    args.append(PLAYBOOK_PATH)

    def _has_invertory():
        return bool(set(('-i', '--inventory-file')).intersection(args))

    if not _has_invertory():
        cwd = os.getcwd()
        hosts = _find_hosts(cwd)
        if not hosts and config.deploy:
            hosts = _gen_hosts(config.deploy)
        if hosts:
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
