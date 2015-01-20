# -*- coding: utf-8 -*-
from distutils.core import setup
import os.path
import sys

import pu


classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]


def read(fname):
    fname = os.path.join(os.path.dirname(__file__), fname)
    if sys.version > '3.0':
        content = open(fname, encoding='utf-8').read()
    else:
        content = open(fname).read().decode('utf-8')
    return content.strip()

def read_files(*fnames):
    return '\r\n\r\n\r\n'.join(map(read, fnames))

setup(
    name = 'pu',
    version=pu.version,
    packages = [
        'pu',
        'pu.aio',
        'pu.aio.protocols',
        'pu.pattern',
        'pu.misc',
        ],
    description = 'Python utils',
    long_description = read_files('README.rst', 'CHANGES.rst'),
    license = 'GNU Library or Lesser General Public License (LGPL)',
    author = 'yuxin',
    author_email = 'ycyuxin@gmail.com',
    url = 'https://github.com/huyx/pu',
    keywords = ['python', 'util'],
    classifiers = classifiers, 
    )
