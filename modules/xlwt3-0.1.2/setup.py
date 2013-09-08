#!/usr/bin/env python
# Python 3.1 port of xlwt http://pypi.python.org/pypi/xlwt by John Machin <sjmachin@lexicon.net>

import sys
import os

from distutils.core import setup

VERSION = '0.1.2'
MAINTAINER_NAME = 'Manfred Moitzi'
MAINTAINER_EMAIL = 'mozman@gmx.at'

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname

DESCRIPTION = (
    'Library to create spreadsheet files compatible with '
    'MS Excel 97/2000/XP/2003 XLS files, '
    'on any platform, with Python 3.1+'
    )

setup(
    name = 'xlwt3',
    version = VERSION,
    maintainer = MAINTAINER_NAME,
    maintainer_email = MAINTAINER_EMAIL,
    url = 'http://bitbucket.org/mozman/xlwt3/wiki/Home',
    download_url = 'http://bitbucket.org/mozman/xlwt3/downloads',
    packages = ['xlwt3', 'xlwt3.excel'],
    provides = ['xlwt3'],
    description = DESCRIPTION,
    long_description = read('README.txt') + read('NEWS.txt'),
    platforms = ['OS Independent'],
    license = 'BSD',
    keywords = ['xls', 'excel', 'spreadsheet', 'workbook'],
    classifiers = [
        'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
