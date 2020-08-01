# -*- coding: utf-8 -*-

import mock


class Handler(object):
    def __init__(self, func, conf=None):
        self.func = func
        self.conf = conf or {}


class MockApp(object):
    def __init__(self):
        self.hook_registry = mock.Mock()
        self.service_name = 'TestService'
        self.api_map = {'ping': Handler(mock.Mock(__name__='ping'))}
        self.thrift_module = mock.Mock(
            TestService=mock.Mock(thrift_services=['ping']))

    def __call__(self):
        pass


app = MockApp()
