#!/usr/bin/env python
# -*- coding: windows-1251 -*-
# Copyright (C) 2005 Kiseliov Roman
#
# This example (also with xlwt-0.7.2) produces an invalid xls-file (Excel 2007)
#
from xlwt3 import *

font0 = formatting.Font()
font0.name = 'Arial'
font1 = formatting.Font()
font1.name = 'Arial Cyr'
font2 = formatting.Font()
font2.name = 'Times New Roman'
font3 = formatting.Font()
font3.name = 'Courier New Cyr'

num_format0 = '0.00000'
num_format1 = '0.000000'
num_format2 = '0.0000000'
num_format3 = '0.00000000'

st0 = XFStyle()
st1 = XFStyle()
st2 = XFStyle()
st3 = XFStyle()
st4 = XFStyle()

st0.font = font0
st0.num_format = num_format0

st1.font = font1
st1.num_format = num_format1

st2.font = font2
st2.num_format = num_format2

st3.font = font3
st3.num_format = num_format3

wb = Workbook()

wb.add_style(st0)
wb.add_style(st1)
wb.add_style(st2)
wb.add_style(st3)

ws0 = wb.add_sheet('0')
ws0.write(0, 0, 'Olya'*0x2000, st0)

wb.save('sst.xls')
