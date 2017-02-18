# -*- coding: utf-8 -*-

import json


def test_gen_hosts(app_yaml):
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
        ret = json.loads(f.read())
    assert ret == {
        'service-deploy': {
            'children': {
                'testing': {
                    'hosts': {
                        'localhost': None,
                        'www.data.com': None,
                        'www.data2.com': None
                    },
                    'vars': {
                        'version': 23543543
                    }
                }
            },
            'vars': {
                'version': 'HEAD',
                'app_name': 'test'
            }
        },
    }
