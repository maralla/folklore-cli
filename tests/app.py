# -*- coding: utf-8 -*-

import mock


class MockApp(object):
    def __init__(self):
        self.hook_registry = mock.Mock()

    def __call__(self):
        pass

app = MockApp()
