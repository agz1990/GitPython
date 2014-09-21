'''
Created on 2013年10月12日

@author: Administrator
'''
from excelInput import ExcleInput
import copy
import excelPack
import unittest
from newAutoBuild import excelInput

xls = 'NewArch.xls';
oneColFileCnt = 27  # 每列可生成27个文件
xlsTableOrder = 'SEBaLITtFGHVRPA'  # 表格中有效列key的顺序
xlsColOrder = 'ADFGHIJKLMNOPQR'  # 表格中有效列头的顺序
outPutFileNum = oneColFileCnt * len(xlsTableOrder)  # 整个表格可生成的文件数
xlsCols = excelPack.getAllColsBySheetIndex(0, xls)
ei = ExcleInput(xls, xlsTableOrder)
xlstTables = [iCol for i, iCol in enumerate(xlsCols)\
           if ExcleInput.CheckOneCol(iCol) is not False \
           and not iCol.insert(0, ExcleInput.CheckOneCol(iCol)) ]

def getRangeByKey(key, begin = 0 , end = None):
    col = xlstTables[xlsTableOrder.index(key)]
    if end == None:
        return col [begin:]
    else:
        return col [begin:end + 1]
difMap = {
          '30': ['S/_16_=向右键切换输入法，向左键表示删除键', 'S/_100_=向左键', 'S/_101_=向右键'],
          '35': ['S/_16_=*键切换输入法,#键输入空格', 'S/_100_=*', 'S/_101_=#']
          }
fileDetails = [
        {'subPath':r'app\main\language',
        'lines':getRangeByKey('S', 3, 14),
        'begin':3,
        'key':'S',
        'encodeType':'gb2312'},

        {'subPath':r'lib\app\libuseraccprivilege\language',
        'lines': getRangeByKey('S', 935),
        'begin':935,
        'key': 'S',
        'encodeType':'gb2312'},

        {'subPath':r'lib\app\libuseraccprivilege\language',
        'lines': getRangeByKey('A', 935),
        'begin':935,
        'key': 'A',
        'encodeType':'utf-8'},

         ]

# schCol = getRangeByKey('S', 3, 14)
# print(schCol)
# for i in range(10):
#     print(ei.tables[i][0:10])

class Test_excelInput(unittest.TestCase):

    def test_CheckOneCol(self):
        '''
        测试一列数据的有效性
        '''
        result = ExcleInput.CheckOneCol(getRangeByKey('S', 3, 14))
        self.assertEqual('S', result)
        pass

    def test_BuildKeysTable(self):
        self.assertEqual(xlsColOrder, ei.colNameOrder)
        self.assertEqual(xlsTableOrder, ei.keyNameOrder)

    def test_GetEncodeType(self):
        cells = [
                 ['gb2312', '简体中文::GB2312'],
                 ['iso8859_6', 'Arabic::ISO8859_6'],
                 ['utf-8', 'Arabic:ISO8859_6'],
                 ['utf-8', '简体中文'],
                 ]
        for cell in cells:
            result = ExcleInput.GetEncodeType(cell[1], '::')
            self.assertEqual(cell[0], result, cell)

    def test_IsSubPathCell(self):
        cells = [
                [r'app\main\language', r'主界面（main）@@ app\main\language'],
                [r'app\mginit\language', r'主菜单（menu）@@ app\mginit\language'],
                [r'app\usermng\language', r'用户管理（APP）@@ app\usermng\language'],
                [r'app\primng\language', r'权限管理（APP）@@ app\primng\language'],
                 ]
        for cell in cells:
            result = ExcleInput.IsSubPathCell(cell[1], '@@')
            self.assertEqual(cell[0], result, cell)

    def test_CheckFormat(self):
        key = 'S'
        et = ExcleInput.FormatErrorType
        cells = [
                   [et['pass'], 'S/_20_=上午'],
                   [et['pass'], '[35]S/_16_=*键切换输入法,#键输入空格'],
                   [et['pass'], '[30]S/_16_=向右键切换输入法，向左键表示删除键'],
                   [et['format'], 'E/_21_=下午'],
                   [et['comment'], '#前面有#的带注释的算检测通过'],
                   [et['empty'], 'S/_16_=']  ,  # 内容字段为空 检测为错误
                   [et['format'], 'S_30_=星期日'],
                   [et['format'], 'S/_31_星期一'],
                   [et['format'], 'S/_A_=上午'],
                   [et['blank'], 'S/_32_=星期  二'],  # 连续俩个空格为错误格式
                   [et['empty'], ''],  # 没有数据为错误格式
                   [et['blank'], '     '],  # 空白字符为错误格式
                   [et['format'], '[3.0]S/_16_=向右键切换输入法，向左键表示删除键'],
               ]

        for cell in cells:
            result = ExcleInput.CheckFormat(cell[1], key)
            self.assertEqual(cell[0], result, cell)

    def test_GetSpecialMap(self):
        ret = ExcleInput.GetSpecialMap(getRangeByKey('S'))
        self.assertDictEqual(difMap, ret)
        pass

    def test_GetNextFileDetailByCol(self):
        schCol = getRangeByKey('S')

        for df in fileDetails:
            col = getRangeByKey(df['key'])
            result = ExcleInput.GetNextFileDetailByCol(col, schCol, df['begin'] - 1)
            self.assertDictContainsSubset(df, result)

    def test_interator(self):
        doWith = ExcleInput.PrintFileInfo
        doWith = None
        for fd in ei:
            ei.SetPlatformName('zmm100_tft35')
            ei.ProcFileInfo(fd, doWith, 'lang', difMap['35'])
        ei.endTarFile()
        self.assertEqual(outPutFileNum, ei.fileCnt)

#     def test_getErrMsgByKey(self):
#         ExcleInput('NewArch.xls').ReportErr()
if __name__ == "__main__":
    import sys
    sys.argv = ['', '-v']
    unittest.main()
