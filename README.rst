Purpose
=======

There is many backup framework, with lots of features, encryption, remote storage, incremental backup, you-name-it... Just to name a few `bup <https://bup.github.io/>`_, `bacula <http://www.bacula.org/>`_, `zbackup <http://zbackup.org/>`_, `duplicity <http://duplicity.nongnu.org/>`_, `zmanda <http://zmanda.com/>`_, etc.

But those projects often focus on file backup. What about in-memory data? What about databases that need data consistency? 

``backupallthethings`` try to alleviate that concern by providing a simple way to backup those services. Also it provide a very simple CLI that allows you to backup anything anytime.

No fancy features, it is the poor man's backup. Files are backuped locally only (ATM). You may then want to rely on those other projects to backup your ... backups.

``backupallthethings`` is a *very* young project and should not be considered stable. The scripts provided to backup each of the services are ... well ... they are what they are. Simple shell scripts; not much safety nets, poor logging / error reporting, may not follow best practices and may seem complete non-sense to experts. 

There is a large `TODO list <https://github.com/devo-ps/backupallthethings#todo>`_, feel free to look into it and hack at will!

Install
=======


From pypi:

.. code-block:: bash

    pip install backupallthethings


Latest:

.. code-block:: bash
    
    pip install git+https://github.com/devo-ps/backupallthethings


Configuration
=============

All the configuration files are available in ``/opt/batt/conf``

Usage
=====

Help
----

Provide extensive help about all the supported options.

.. code-block:: bash
    
    batt -h


List supported services
-----------------------

List the scripts that are enabled when ran without parameters

.. code-block:: bash
    
    batt list 


Add / Remove service to the defaults
------------------------------------

Add / remove support for the services' backup scripts. Note that it only applies when ran without parameters.

.. code-block:: bash

    # Add support for the mysql / file and postgresql services
    sudo batt enable mysql file postgresql
    
    # Disable (if enabled previously) the support for redis and mongodb
    sudo batt disable redis mongodb


The logic is similar to Apache/Nginx ``sites-enabled``. ``batt`` creates links to the real script in ``/opt/batt/scripts-enabled`` and remove those links when disabling services.

You need to run the enable/disable feature as ``root`` due to the permissions.

Run Backup
----------

**Run backup for the enabled services**

When ran without parameters, ``batt`` will attempt to run every enabled backup script and use their respective configuration files.

.. code-block:: bash

    sudo batt


You need to run the backup as ``root``.

**Run custom backup**

When passing parameters to the ``batt`` command, it will effectively bypass the default enabled services and attempt to run each of the service provided on the command line.

.. code-block:: bash
    
    # Will run the mysql and file backup scripts with the default values provided in
    # the script and config file.
    sudo batt mysql file
    
    # Will backup only the ``wordpress`` database and the ``/var/www/wordpress`` folder
    sudo batt mysql file --mysql-db wordpress --file /var/www/wordpress
    
    # Same as above; the service ``mysql`` and ``file`` can be ommitted as they are 
    # implicitely defined by the 
    # `--mysql-db` and `--file` options
    sudo batt --mysql-db wordpress --file /var/www/wordpress
    
    # You can specify options multiple times as well; it will backup both the 
    # wordpress and mysql databases (in different files)
    sudo batt --mysql-db wordpress --mysql-db mysql


**Custom destination folder**

By default the backup archives will be saved in ``/opt/backup/YYYY/MM/DD/{service}``. Beware that the former files will be overwritten if they already exist.

You can change the path of the destination folder to be more granular or fully custom with the ``--path`` argument.

.. code-block:: bash

    # Will put the backup archives in ``/custom/path/{service}``
    sudo batt --path /custom/path
    
    # You can specify date patterns (e.g. ``/opt/backup/2014/11/13/22/53/{service}``)
    sudo batt --path /opt/backup/%Y/%m/%d/%H/%M
    
    # Another ... ``/opt/backup/2014/11/13/daily/{service}``
    sudo batt --path /opt/backup/%Y/%m/%d/daily


More details about the date format is available `here <https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior>`_.

Architecture
============

batt
-------------

Python based script, effectively parses the various arguments and manage the services list. Then it delegates the work to the services scripts.

backup scripts
--------------

They are stored in ``/opt/batt/scripts-available``.

In practice they can be based on any language; shell, python, ruby, etc. as long as they follow the naming convention ``backup-{service}`` and are executable.

The ``BATT_DEST`` ENV variable is passed to them and define the prefix path where to store the resulting backup archive.

Space separated arguments are passed to the script (databases, files, etc.) that the script may choose to use or ignore.

backup scripts: any language; currently mostly shell script to make use of the regular shell commands.

TODO
====

Lots of things to do... A quick list below non-prioritized.

- Better best practices for each of the service' backup logic
- Better error management
- Use log file / syslog
- Remote storage (S3 / etc.)
- Restore
- Notification (email / etc.)
- More technologies
- More flexible command; allow drop in place of technologies
- Documentation; how to add scripts, etc.
- Better configuration support
- Purge backup support (e.g. after 7 days)
- MySQL transaction vs lock for InnoDB / MyISAM
- Handle LVM based backup (and more generally snapshot capable filesystems like ZFS)

Disclaimer
==========

The ``batt`` tool is in early development stage and may break, erase data, corrupt filesytem, burn trees, spill coffee on your keyboard and may even be responsible for global warming (who knows!). Use at your own risk. `devo.ps <http://devo.ps/>`_ is in no way responsible in the event of something wrong happen.

License
=======

MIT
