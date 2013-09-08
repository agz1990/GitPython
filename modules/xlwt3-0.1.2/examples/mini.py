#!/usr/bin/env python
# Copyright (C) 2005 Kiseliov Roman

from xlwt3 import *

w = Workbook()
ws = w.add_sheet('xlwt was here')
w.save('mini.xls')
