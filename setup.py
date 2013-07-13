#!/usr/bin/env python

import os
import sys
import hound

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist register upload')
    sys.exit()

packages = ['hound']
requires = ['watchdog==0.6.0',
            'docopt==0.6.1']

setup(
    name='caffeinated-hound',
    version=hound.__version__,
    packages=packages,
    license=open('LICENSE.txt').read(),
    description='CoffeeScript watcher and compiler.',
    long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    author='Marconi Moreto',
    author_email='caketoad@gmail.com',
    url='https://github.com/marconi/caffeinated-hound',
    zip_safe=False,
    package_data={'': ['LICENSE.txt']},
    install_requires=requires,
    entry_points={'console_scripts': ['hound = hound.scripts:hound_cmd']}
)
