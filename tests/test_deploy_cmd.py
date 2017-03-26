# -*- coding: utf-8 -*-

import pytest
import mock
import tempfile
from docopt import DocoptExit
from takumi_cli.cmds.deploy import run
from takumi_cli.deploy import PLAYBOOK_PATH
import ansible.cli.playbook


@pytest.fixture
def mock_ansible():
    with mock.patch.object(ansible.cli.playbook, 'PlaybookCLI') as m:
        yield m


@pytest.fixture
def mock_tempfile():
    tempf = tempfile.mktemp()
    with mock.patch.object(tempfile, 'mktemp', return_value=tempf) as m:
        yield tempf
    m.assert_called_with()


def test_command_invalid():
    with pytest.raises(DocoptExit) as e:
        run([])
    assert 'Usage' in str(e.value)

    with pytest.raises(DocoptExit) as e:
        run(['--'])
    assert 'Usage' in str(e.value)


def test_command(mock_ansible, mock_tempfile):
    run(['testing'])
    mock_ansible.assert_called_with([
        'ansible-playbook',
        '--limit', 'testing',
        '--inventory-file', mock_tempfile,
        PLAYBOOK_PATH,
    ])


def test_command_tag(mock_ansible, mock_tempfile):
    run(['testing', '-t', 'deploy,cron'])
    mock_ansible.assert_called_with([
        'ansible-playbook',
        '--limit', 'testing',
        '--tags', 'deploy,cron',
        '--inventory-file', mock_tempfile,
        PLAYBOOK_PATH,
    ])


def test_command_deploy(mock_ansible, mock_tempfile):
    run(['testing', '-t', 'deploy', '-p', 'system.yml'])
    mock_ansible.assert_called_with([
        'ansible-playbook',
        '--limit', 'testing',
        '--tags', 'deploy',
        '--inventory-file', mock_tempfile,
        'system.yml'
    ])


def test_command_ansible_args(mock_ansible, mock_tempfile):
    run(['testing', '--', '--ask-pass'])
    mock_ansible.assert_called_with([
        'ansible-playbook',
        '--ask-pass',
        '--limit', 'testing',
        '--inventory-file', mock_tempfile,
        PLAYBOOK_PATH
    ])


def test_command_pure_ansible(mock_ansible):
    run(['--', '-i', 'hosts', '-t', 'hello', 'playbook.yml'])
    mock_ansible.assert_called_with([
        'ansible-playbook', '-i', 'hosts', '-t', 'hello',
        'playbook.yml'])
