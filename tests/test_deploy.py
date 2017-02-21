# -*- coding: utf-8 -*-


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
    temp_host = _gen_hosts(data)
    with open(temp_host) as f:
        ret = f.read()
    assert ret == """[testing]
localhost
www.data.com
www.data2.com
[testing:vars]
version=23543543
[service-deploy:children]
testing
[service-deploy:vars]
app_name=test
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
    temp_host = _gen_hosts(data)
    with open(temp_host) as f:
        ret = f.read()
    assert ret == """[testing]
localhost

[service-deploy:children]
testing
[service-deploy:vars]
app_name=test
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
    temp_host = _gen_hosts(data)
    with open(temp_host) as f:
        ret = f.read()
    assert ret == """[testing]
localhost version=123
www.data.com
www.data2.com
[testing:vars]
version=23543543
[service-deploy:children]
testing
[service-deploy:vars]
app_name=test
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
    temp_host = _gen_hosts(data)
    with open(temp_host) as f:
        ret = f.read()
    assert ret == """[testing]
localhost
[testing:vars]
version=23543543
[service-deploy:children]
testing
[service-deploy:vars]
app_name=test
version=HEAD"""
