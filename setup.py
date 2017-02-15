#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='takumi_cli',
    version='0.1.0',
    description='Takumi service framework command line toolkit',
    long_description=open("README.rst").read(),
    author="Eleme Lab",
    author_email="imaralla@icloud.com",
    packages=find_packages(),
    package_data={'': ['LICENSE', 'README.rst']},
    url='https://github.com/elemecreativelab/takumi-cli',
    install_requires=[
        'docopt==0.6.2',
        'schema==0.6.5',
    ],
    entry_points={
        'console_scripts': [
            'takumi = takumi_cli.cmds:main'
        ]
    }
)
