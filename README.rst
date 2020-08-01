folklore-cli: Folklore command line toolkit
=======================================

.. image:: https://travis-ci.org/maralla/folklore-cli.svg?branch=master
    :target: https://travis-ci.org/maralla/folklore-cli

Command line tool for managing Folklore services.

Install
-------

.. code:: bash

    $ pip install folklore-cli

Usage
-----

.. code-block:: bash

    $ folklore -h

Run Folklore service
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ folklore serve

Deploy an application
~~~~~~~~~~~~~~~~~~~~~

To deploy using ansible, extra requirements should be installed:

.. code:: bash

    $ pip install folklore-cli[deploy]


Add ``deploy`` entry to *app.yaml*:

.. code:: yaml

    deploy:
      vars:
        version: HEAD
      targets:
        testing:
          - localhost
          - testing.com
        prod:
          - app.prod

Using the following command to deploy:

.. code-block:: bash

    $ folklore deploy testing -t deploy

The deploy command is implemented using `ansible <https://github.com/ansible/ansible>`_.

To deploy crontab, add the following config to *app.yaml*

.. code-block:: yaml

    deploy:
      crontab:
        - name: check dirs
          schedule: "0 5,2 * * *"
          job: 'ls -alh > /dev/null'

        - name: say hello
          schedule:
            minute: 0
            hour: 5,2
          job: 'scripts/say_hello.py'

then run:

.. code-block:: bash

    $ folklore deploy <target> -t cron

Cron jobs are run under app working directory ``/srv/{{ app_name }}``.

Start an interactive shell
~~~~~~~~~~~~~~~~~~~~~~~~~~

To start an IPython shell, extra requirements should be installed:

.. code:: bash

    $ pip install folklore-cli[shell]

Start the shell:

.. code:: bash

    $ folklore shell -t <host> -- <ipython args>
