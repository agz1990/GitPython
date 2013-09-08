'''
Created on 2013年9月6日

@author: hp41
'''


import xlrd3

'''
本代码主要封装了几个操作Excel数据的方法
'''
resourceExcle = r'.\resource\sourceLanguage.xls'

# 获取行视图
# 根据Sheet序号获取该Sheet包含的所有行，返回值类似[ ['a', 'b', 'c'], ['1', '2', '3'] ]
# sheetIndex指示sheet的索引，0表示第一个sheet，依次类推
# xlsFilePath是Excel文件的相对或者绝对路径

def getAllRowsBySheetIndex(sheetIndex, xlsFilePath):
    workBook = xlrd3.open_workbook(xlsFilePath)
    table = workBook.sheets()[sheetIndex]
    
    rows = []
    rowNum = table.nrows # 总共行数
    rowList = table.row_values
    for i in range(rowNum):
        rows.append(rowList(i)) # 等价于rows.append(i, rowLists(i))
    
    return rows


'''
获取某个Sheet的指定序号的行
sheetIndex从0开始
rowIndex从0开始
'''
def getRow(sheetIndex, rowIndex, xlsFilePath):
    rows = getAllRowsBySheetIndex(sheetIndex, xlsFilePath)
    
    return rows[rowIndex]


''' 
    获取列视图
    根据Sheet序号获取该Sheet包含的所有列，返回值类似[ ['a', 'b', 'c'], ['1', '2', '3'] ]
    sheetIndex指示sheet的索引，0表示第一个sheet，依次类推
    xlsFilePath是Excel文件的相对或者绝对路径
'''
def getAllColsBySheetIndex(sheetIndex, xlsFilePath):
    workBook = xlrd3.open_workbook(xlsFilePath)
    table = workBook.sheets()[sheetIndex]
    
    cols = []
    colNum = table.ncols # 总共列数
    colList = table.col_values
    for i in range(colNum):
        cols.append(colList(i))
    
    return cols


'''
获取某个Sheet的指定序号的列
sheetIndex从0开始
colIndex从0开始
'''
def getCol(sheetIndex, colIndex, xlsFilePath):
    cols = getAllColsBySheetIndex(sheetIndex, xlsFilePath)   
    return cols[colIndex]


'''
获取指定sheet的指定行列的单元格中的值
'''
def getCellValue(sheetIndex, rowIndex, colIndex, xlsFilePath):
    workBook = xlrd3.open_workbook(xlsFilePath)
    table = workBook.sheets()[sheetIndex]
    
    return table.cell(rowIndex, colIndex).value # 或者table.row(0)[0].value或者table.col(0)[0].value


if __name__=='__main__':
    pass
#     rowsInFirstSheet = getAllRowsBySheetIndex(0,resourceExcle)
#     print(rowsInFirstSheet)
#     colsInFirstSheet = getAllColsBySheetIndex(0, resourceExcle)
#     print(getRow(0, 0, resourceExcle)) # 获取第一个sheet第一行的数据