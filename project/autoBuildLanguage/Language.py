'''
Created on 2013年9月7日

@author: agz
'''
import excelPack
import os
import string
import Rules

class LangageObj():
    def __init__(self, xlsObj, encodingMap, \
                 destPath='.', AppMap={'中文':''}, ExclueMap=[]):
        self.xls = xlsObj
        self.keymap = encodingMap  # 获取 编码格式对应表
        self.appmap = AppMap  # 获取要生成文件的对应表
        self.delmap = ExclueMap  # 不同平台需要排除的字段表
        self.encodType = 'utf-8'  # 当前语言的编码格式
        self.curFileName = ''  # 当前语言的文件名字
        self.curFileObj = None  # 生成当前文件的操作句柄
        self.key = ''  # 当前语言的  key 值
        self.col = 65  # 程序运行实时列数 （A）
        self.row = 0  # 程序运行实时行数
        self.preLine = ''  # 上一个有效行
        self.curline = ''  # 当前行
        self.hint = ''  # 全局提示
        self.dest = destPath  # 目标生成目标路径
        self.subdir = 'lang'  # 小写  key 语言的存放路径前缀
        self.ChieseCol = self.getRolByKey('S')

    def xprint(self):
        if len(self.hint) != 0:
            print('\t\t', self.hint)

    # 检查一列数据是否是有效数据,如果是获得 对于的key值，与文件名
    def getColDetail(self, cloObj):
        # 检查键值有效性
        Error = None
        try:
            key = 'S'
            key = cloObj[10][0]
            if key not in self.keymap:
                self.hint = ('\n\t *** Warning col:%c  Discover a empty col ! ****') % (chr(self.col))
                return Error

            self.key = key
            self.encodType = self.keymap[key]
            self.curFileName = 'LANGUAGE.' + self.key
            return True

        except IndexError:  # 无效列处理
            self.hint = ('\n\t *** Warning col:%c  Discover a empty col ! ****') % (chr(self.col))
            return Error

    # 检查一行数据的有效性
    def checkFormat(self, strline, key=None):
        if key is not None:
            head = key + '/_'
        else:
            head = self.key + '/_'
        return strline.startswith(head)
    #
    def checkAndEncodingOneLine(self, aline):
        aline = aline.strip(string.whitespace)
        schLine = self.ChieseCol[self.row - 1]
        if self.checkFormat(aline) is True:
            if schLine in self.delmap:  # 排除 Map 中的项
                self.hint = '-*- Warning 【%c:%04d】   exclude 【%s】 -*-' % (chr(self.col), self.row, aline)
                return False
            # 字符串有效
            line = aline + os.linesep
            try:
                return line.encode(self.encodType)  # 把 utf-8 格式转化成指定编码
            except UnicodeEncodeError:
                self.hint = '*** Error 【%c:%04d】  Coding %s 【%s】 ***' % (chr(self.col), self.encodType, aline[0:aline.find('=')])
                return False
        elif schLine in self.appmap:  # 生成路径控制数据不做处理
            self.hint = ''
            return False
        elif len(schLine) == 0 :  # 忽略无效行
            self.hint = ''
            return False
        elif self.checkFormat(schLine, 'S') is False:  # 排除中文无效项目对应的项
            self.hint = ''
            return False
        else:
            self.hint = '*** Error 【%c:%04d】  Format error  【%s】 ***' % (chr(self.col), self.row, aline)
            return False

    def upDadeFileObj(self, aline):
        cell = aline.strip(string.whitespace)
#         print(cell)
        if cell in self.appmap:
            try:
                self.curFileObj.close()  # 关闭前一个文件
#                 print(' ***  Close a file : 【%c:%04d】  *** '%(chr(self.col),self.row))
            except AttributeError:
                pass  # 忽略第一个打开

            # 组装文件名
            if self.key in string.ascii_lowercase:  # 小写key要添加 sub_dir 路径
                finalPath = os.path.join(self.dest, self.appmap[cell], self.subdir)
            else:
                finalPath = os.path.join(self.dest, self.appmap[cell])

            finalName = os.path.join(finalPath, self.curFileName)
#             print('\n\t Destfile: ', finalName)
            if not os.path.exists(finalPath):
                os.makedirs(finalPath)
            self.curFileObj = open(finalName, 'bw')
            return True
        else:
            return False

    # 解析一个 Excel 数据表
    def buildOneLanuageFile(self, cloObj, keys=None):

            self.row = 0
            if self.getColDetail(cloObj) is None:
                self.xprint();
                return

            if keys is None:
                keys = self.keymap

            if self.key not in keys:
                return None

            print('\nExcelfile: %s============\n\t Discover a valid  col: %c  key: LANGUAGE.%s' % (self.xls, chr(self.col), self.key))
            for aline in cloObj:
                self.row = self.row + 1
                self.upDadeFileObj(self.ChieseCol[self.row - 1])  # 通过中文列 获取需要生成文件的目标
                try:  # 检查文件数据有效性
                    self.curFileObj.write(self.checkAndEncodingOneLine(aline))
#                     print('\t\t>> ', aline)
                except TypeError:
                    self.xprint();
                    continue
                except AttributeError :  # 忽略文件第一次中文列表，一开始内容  不在  self.appmap 的情况
                    continue
            self.row = 0
    def buildOneExcelFile(self, keys=None, sheetIndex=0):
        for icol in excelPack.getAllColsBySheetIndex(sheetIndex, self.xls):
            self.buildOneLanuageFile(icol, keys)
            self.col = self.col + 1
        self.col = 65

    # 通过 key 值获取对应列
    def getRolByKey(self, key, sheetIndex=0):
        for icol in excelPack.getAllColsBySheetIndex(sheetIndex, self.xls):
            if self.getColDetail(icol) is True:
                if self.key == key:
                    return icol



def buildSheets(xlss):
    for fileName in xlss:
        dest_dir = 'obj\\' + fileName[0:fileName.find('.xls')]
        xobj = LangageObj(fileName, Rules.CodeingMap, \
                          dest_dir, Rules.AppMap, Rules.ExclueMap30)

#         xobj = LangageObj(fileName, Rules.CodeingMap, dest_dir)

        xobj.buildOneExcelFile(Rules.ValidKeys)

def main():
    # 获取当前路径下 所有 Excel 表集合
    xlss = [xls for xls in os.listdir(path='.') if xls.endswith('.xls')]
    buildSheets(xlss)
    print('done...')


def testCmp():
    xobj1 = LangageObj('NewArch.xls', Rules.CodeingMap)
    xobj2 = LangageObj('NewArch2.xls', Rules.CodeingMap)
    compareXbojs(xobj1, xobj2, 'B')

# 必须保证中文是不修改的情况下进行对比，默认比较中文
def compareXbojs(xls1, xls2, key='S'):

    iRow = 1
    iCnt = 1
    if key not in 'ST':
        ChineseCol = xls1.ChieseCol
        keyCol1 = xls1.getRolByKey(key)
        keyCol2 = xls2.getRolByKey(key)
        for iSCH in ChineseCol:
            try:
                if keyCol1[iRow] != keyCol2[iRow]:
                    print('%2d:中文  【%s】   R:%3d -- 原 :【%s】  ==>【%s】  '\
                          % (iCnt, iSCH, iRow, keyCol1[iRow], keyCol2[iRow]))
                    iCnt += 1
            except IndexError:
                print('**************')
                continue
            iRow += 1
    else:  # 简体中文与繁体中文不需要参考
        keyCol1 = xls1.getRolByKey(key)
        keyCol2 = xls2.getRolByKey(key)
        for iSCH in keyCol1:
            try:
                if keyCol1[iRow] != keyCol2[iRow]:
                    print('%2d: R:%3d -- 原 :【%s】  ==>【%s】  '\
                          % (iCnt, iRow, keyCol1[iRow], keyCol2[iRow]))
                    iCnt += 1
            except IndexError:
                print('**************')
                continue
            iRow += 1



if __name__ == '__main__':
#     main()
    testCmp()
    pass
