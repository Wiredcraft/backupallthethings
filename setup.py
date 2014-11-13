#!/usr/bin/env python
import os
import sys
import shutil
from glob import glob

from devopsbackup import __version__, __author__, __author_email__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

base_install = '/opt/devops/backup'

data_files = []
data_files.append((os.path.join(base_install, 'conf'), glob('./conf/*.conf')))
data_files.append((os.path.join(base_install, 'scripts-available'), glob('./scripts-available/*')))
data_files.append((os.path.join(base_install, 'scripts-enabled'), []))

setup(
    name='devopsbackup',
    version=__version__,
    description='devops-backup is a simple to extend collectin of backup scripts',
    url = 'https://github.com/devo-ps/devops-backup',
    author=__author__,
    author_email=__author_email__,
    license='MIT',
    package_dir={ 
        'devopsbackup': 'devopsbackup'
    },
    packages=[
       'devopsbackup'
    ],
    scripts=[
        'bin/devops-backup'
    ],
    data_files=data_files
)