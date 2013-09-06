#!/usr/bin/env python
# Python 3.1 port of xlrd http://www.lexicon.net/sjmachin/xlrd.htm by John Machin <sjmachin@lexicon.net>

import sys
import os

from distutils.core import setup

VERSION = '0.1.4'
MAINTAINER_NAME = 'Manfred Moitzi'
MAINTAINER_EMAIL = 'mozman@gmx.at'

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname
setup(
    name = 'xlrd3',
    version = VERSION,
    maintainer = MAINTAINER_NAME,
    maintainer_email = MAINTAINER_EMAIL,
    url = 'http://bitbucket.org/mozman/xlrd3/wiki/Home',
    download_url = 'http://bitbucket.org/mozman/xlrd3/downloads',
    packages = ['xlrd3'],
    provides = ['xlrd3'],
    description = 'Library for developers to extract data from Microsoft Excel (tm) spreadsheet files',
    long_description = read('README.txt')+read('NEWS.txt'),
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
		'Topic :: Software Development :: Libraries :: Python Modules',
		],
)
