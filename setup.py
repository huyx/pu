# -*- coding: utf-8 -*-
from distutils.core import setup
from pu import version
import os.path


classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]


def read(fname):
    fname = os.path.join(os.path.dirname(__file__), fname)
    return open(fname, encoding='utf-8').read().strip()

def read_files(*fnames):
    return '\r\n\r\n\r\n'.join(map(read, fnames))

setup(
    name = 'pu',
    version = version,
    packages = [
        'pu',
        'pu.aio',
        'pu.aio.protocols',
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
