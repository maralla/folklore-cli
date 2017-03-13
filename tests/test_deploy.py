# -*- coding: utf-8 -*-

import mock
import os


def test_gen_hosts1(app_yaml):
    # vars:
    #   version: HEAD
    # targets:
    #   testing:
    #     hosts:
    #       - localhost
    #       - www.data.com
    #       - www.data2.com
    #     vars:
    #       version: 23543543
    from takumi_cli.deploy import _gen_hosts
    data = {
        'targets': {
            'testing': {
                'hosts': ['localhost', 'www.data.com', 'www.data2.com'],
                'vars': {
                    'version': 23543543
                }
            }
        },
        'vars': {
            'version': 'HEAD'
        }
    }
    with mock.patch.object(os, 'getcwd', return_value='repo_path'):
        temp_host = _gen_hosts(data)
    with open(temp_host) as f:
        ret = f.read()
    assert ret == """[testing]
localhost
www.data.com
www.data2.com
[testing:vars]
env=testing
version=23543543
[service-deploy:children]
testing
[service-deploy:vars]
app_name=test
app_repo=repo_path
crontabs=[]
version=HEAD"""


def test_gen_hosts2(app_yaml):
    # targets:
    #   testing: localhost
    # vars:
    #   version: HEAD
    from takumi_cli.deploy import _gen_hosts
    data = {
        'targets': {
            'testing': 'localhost',
        },
        'vars': {
            'version': 'HEAD'
        }
    }
    with mock.patch.object(os, 'getcwd', return_value='repo_path'):
        temp_host = _gen_hosts(data)
    with open(temp_host) as f:
        ret = f.read()
    assert ret == """[testing]
localhost
[testing:vars]
env=testing
[service-deploy:children]
testing
[service-deploy:vars]
app_name=test
app_repo=repo_path
crontabs=[]
version=HEAD"""


def test_gen_hosts3(app_yaml):
    # vars:
    #   version: HEAD
    # targets:
    #   testing:
    #     hosts:
    #       - localhost:
    #           version: 123
    #       - www.data.com
    #       - www.data2.com
    #     vars:
    #       version: 23543543
    from takumi_cli.deploy import _gen_hosts
    data = {
        'targets': {
            'testing': {
                'hosts': [
                    {'localhost': {'version': 123}},
                    'www.data.com',
                    'www.data2.com'
                ],
                'vars': {
                    'version': 23543543
                }
            }
        },
        'vars': {
            'version': 'HEAD'
        }
    }
    with mock.patch.object(os, 'getcwd', return_value='repo_path'):
        temp_host = _gen_hosts(data)
    with open(temp_host) as f:
        ret = f.read()
    assert ret == """[testing]
localhost version=123
www.data.com
www.data2.com
[testing:vars]
env=testing
version=23543543
[service-deploy:children]
testing
[service-deploy:vars]
app_name=test
app_repo=repo_path
crontabs=[]
version=HEAD"""


def test_gen_hosts4(app_yaml):
    # vars:
    #   version: HEAD
    # targets:
    #   testing:
    #     hosts: localhost
    #     vars:
    #       version: 23543543
    from takumi_cli.deploy import _gen_hosts
    data = {
        'targets': {
            'testing': {
                'hosts': 'localhost',
                'vars': {
                    'version': 23543543
                }
            }
        },
        'vars': {
            'version': 'HEAD'
        }
    }
    with mock.patch.object(os, 'getcwd', return_value='repo_path'):
        temp_host = _gen_hosts(data)
    with open(temp_host) as f:
        ret = f.read()
    assert ret == """[testing]
localhost
[testing:vars]
env=testing
version=23543543
[service-deploy:children]
testing
[service-deploy:vars]
app_name=test
app_repo=repo_path
crontabs=[]
version=HEAD"""


def test_convert_crontab(app_yaml):
    input_data = [
        {
            'job': 'ls -alh > /dev/null',
            'name': 'check dirs',
            'schedule': '0 5,2 * * *'
        },
        {
            'job': 'scripts/say_hello.py',
            'name': 'say hello',
            'schedule': {
                'hour': '5,2',
                'minute': 0
            }
        }
    ]
    from takumi_cli.deploy import _convert_crontab
    ret = _convert_crontab(input_data)
    assert ret == [
        {
            'month': '*', 'hour': '5,2', 'minute': '0', 'day': '*',
            'name': 'check dirs',
            'work_job': 'cd /srv/test && ls -alh > /dev/null',
            'job': 'ls -alh > /dev/null',
            'schedule': '0 5,2 * * *', 'weekday': '*'
        }, {
            'hour': '5,2', 'job': 'scripts/say_hello.py',
            'minute': 0, 'schedule': {'minute': 0, 'hour': '5,2'},
            'name': 'say hello',
            'work_job': 'cd /srv/test && scripts/say_hello.py'
        }]
