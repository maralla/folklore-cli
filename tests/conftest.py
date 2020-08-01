# -*- coding: utf-8 -*-

import mock
import pytest
import os
import sys

DIRNAME = os.path.dirname(__file__)
APP_YAML_PATH = os.path.join(DIRNAME, 'app.yaml')


@pytest.fixture
def app_yaml():
    with mock.patch.dict(
            os.environ, {'FOLKLORE_APP_CONFIG_PATH': APP_YAML_PATH}):
        yield


@pytest.fixture
def gunicorn_serve():
    with mock.patch.object(sys, 'argv', ['folklore', 'serve']):
        yield
