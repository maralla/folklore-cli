# -*- coding: utf-8 -*-

"""
takumi_cli.deploy
~~~~~~~~~~~~~~~~~

Implement deploy command using ansible.
"""

import json
import os
import tempfile
from takumi_config import config

PLAYBOOK_PATH = os.path.join(
    os.path.dirname(__file__), 'playbook', 'playbook.yml')


def _find_hosts(cwd):
    hosts = os.path.join(cwd, 'hosts')
    if os.path.exists(hosts):
        return hosts


def _vars(d):
    return ['{}={}'.format(k, v) for k, v in sorted(d.items())]


def _convert_section(name, data):
    hosts = data.get('hosts', [])
    group_vars = data.get('vars', {})

    items = ['[{}]'.format(name)]
    for host_name, host_vars in sorted(hosts.items()):
        item = [host_name]
        item.extend(_vars(host_vars))
        items.append(' '.join(item))

    section = '\n'.join(items)

    var_section = ''
    if group_vars:
        var_items = '\n'.join(_vars(group_vars))
        var_section = '[{}:vars]\n{}'.format(name, var_items)
    return [section, var_section]


def _convert_hosts(hosts):
    section_names = []
    sections = []
    for k, v in sorted(hosts.items()):
        converted = {}
        if not isinstance(v, dict):
            v = {'hosts': v}
        hs = v.get('hosts', [])
        if isinstance(hs, str):
            hs = [hs]
        for item in hs:
            if not isinstance(item, dict):
                item = {item: {}}
            converted.update(item)
        v['hosts'] = converted
        sections.extend(_convert_section(k, v))
        section_names.append(k)
    return sections, section_names


def _convert_crontab(data):
    working_dir = '/srv/{}'.format(config.app_name)
    items = []
    for item in data:
        sched = item.get('schedule')
        if isinstance(sched, str):
            minute, hour, day, month, weekday = sched.split()
            sched = {
                'minute': minute,
                'hour': hour,
                'day': day,
                'month': month,
                'weekday': weekday
            }
        item.update(sched)
        item['work_job'] = 'cd {} && {}'.format(working_dir, item['job'])
        items.append(item)
    return items


def _gen_hosts(deploy_config):
    hosts = deploy_config.get('targets', {})
    sections, section_names = _convert_hosts(hosts)

    crontab = _convert_crontab(deploy_config.get('crontab', []))
    deploy_vars = deploy_config.get('vars', {})
    deploy_vars['app_name'] = config.app_name
    deploy_vars['crontabs'] = json.dumps(crontab)

    main_section = ['[service-deploy:children]']
    main_section.extend(section_names)
    sections.append('\n'.join(main_section))

    main_vars = ['[service-deploy:vars]']
    main_vars.extend(_vars(deploy_vars))
    sections.append('\n'.join(main_vars))

    hosts_file = tempfile.mktemp()
    with open(hosts_file, 'w') as f:
        f.write('\n'.join(sections))
    return hosts_file


def _compose_args(target, args):
    if '--limit' not in args:
        args.extend(['--limit', target])
    args.append(PLAYBOOK_PATH)

    def _has_invertory():
        return bool(set(('-i', '--inventory-file')).intersection(args))

    cwd = os.getcwd()
    if not _has_invertory():
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
