#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test_mini
# Created: 03.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import os
import unittest
import filecmp

import xlwt3

def from_tst_dir(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

class TestMini(unittest.TestCase):
    def test_create_mini_xls(self):
        book = xlwt3.Workbook()
        sheet = book.add_sheet('xlwt was here')
        book.save('mini.xls')

        self.assertTrue(filecmp.cmp(from_tst_dir('mini.xls'),
                                    from_tst_dir(os.path.join('output-0.7.2', 'mini.xls')),
                                    shallow=False))

if __name__=='__main__':
    unittest.main()