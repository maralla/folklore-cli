takumi-cli: Takumi command line toolkit
=======================================

Command line tool for managing Takumi services.

Usage
-----

General usage:

.. code-block:: bash

    $ takumi -h

To run a Takumi service

.. code-block:: bash

    $ takumi serve

Deploy

.. code-block:: bash

    # <target> is the cluster or host name defined in app.yaml
    # or ansible inventory file.
    # <ansible_args> is then extra arguments passed to ansible-playbook.
    $ takumi deploy <target> <ansible_args>
