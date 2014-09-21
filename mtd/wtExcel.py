'''
Created on 2013年9月8日

@author: agz
'''
from datetime import datetime
import xlwt3

def main():
    style0 = xlwt3.easyxf('font: name Times New Roman, color-index red, bold on',
                         num_format_str='#,##0.00')
    style1 = xlwt3.easyxf(num_format_str='D-MMM-YY')

    wb = xlwt3.Workbook()
    ws = wb.add_sheet('A Test Sheet')

    ws.write(0, 0, 1234.56, style0)
    ws.write(1, 0, datetime.now(), style1)
    ws.write(2, 0, 1)
    ws.write(2, 1, 1)
    ws.write(2, 2, xlwt3.Formula("A3+B3"))

    wb.save('example.xls')
if __name__ == '__main__':
    main()
    pass
