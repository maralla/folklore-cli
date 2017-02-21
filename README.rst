takumi-cli: Takumi command line toolkit
=======================================

.. image:: https://travis-ci.org/elemepi/takumi-cli.svg?branch=master
    :target: https://travis-ci.org/elemepi/takumi-cli

Command line tool for managing Takumi services.

Usage
-----

General usage:

.. code-block:: bash

    $ takumi -h

To run a Takumi service

.. code-block:: bash

    $ takumi serve

To deploy an application:

.. code-block:: bash

    # <target> is the cluster or host name defined in app.yaml
    # or ansible inventory file.
    # <ansible_args> is then extra arguments passed to ansible-playbook.
    $ takumi deploy <target> <ansible_args>

The deploy command is implemented using `ansible <https://github.com/ansible/ansible>`_.
