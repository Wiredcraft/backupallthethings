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
data_files.append((os.path.join(base_install, 'conf'), glob('./conf/*.conf.template')))
data_files.append((os.path.join(base_install, 'scripts-available'), glob('./scripts-available/*')))

setup(
    name='devopsbackup',
    version=__version__,
    description='devops-backup is a simple to extend collectin of backup scripts',
    url = 'https://github.com/devo-ps/devops-backup',
    author=__author__,
    author_email=__author_email__,
    license='MIT',
    install_requires=['docopt'],
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

# We don't want it to be managed by setup and loose the default on install
scripts_enabled = os.path.join(base_install, 'scripts-enabled')
if not os.path.exists(scripts_enabled):
    os.makedirs(scripts_enabled)

# We ship default config files as .template - need to set them as default if not
# present yet
conf_dir = os.path.join(base_install, 'conf')
for template in os.listdir(conf_dir):
    if not template.endswith('.template'):
        continue
    srv_conf = template.replace('.template','')

    src = os.path.join(conf_dir, template)
    dest = os.path.join(conf_dir, srv_conf)
    
    if os.path.exists(dest):
        sys.stderr.write('Config file %s already present. Skipping.\n' % dest)
        continue

    shutil.copy2(src, dest)

