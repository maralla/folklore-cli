#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='folklore_cli',
    version='0.1.2',
    description='Folklore service framework command line toolkit',
    long_description=open("README.rst").read(),
    author="maralla",
    author_email="imaralla@icloud.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/maralla/folklore-cli',
    install_requires=[
        'folklore',
        'folklore-ext',
        'folklore-config',
        'docopt',
        'schema',
        'gevent>=1.2.1',
        'thriftpy',
        'gunicorn',
    ],
    extras_require={
        'deploy': ['ansible>=2.2.0.0'],
        'shell': ['folklore-client', 'IPython']
    },
    entry_points={
        'console_scripts': [
            'folklore = folklore_cli.cmds:main'
        ]
    }
)
