'''
Created on 2013年9月7日

@author: agz
'''


import NewArchRules as Rules
from string import Template
import excelPack
import os
import re
import string
eEncode = Template('*** ***')
eFormat = Template('*** ***')


# 检查一行数据的有效性
def checkFormat(strline, key):
    PCheckFormart = re.compile(r'''
                    ^(?P<key>[A-Za-z])    # 匹配键值
                    /_(?P<num>\d+)_=      # 匹配中间字符
                    (?P<value>.+)         # 匹配字段值
                ''', re.X)

    if not PCheckFormart.match(strline):
        return None
    if re.search(r''' \s+|\s$''', strline):  # 检查连续空格数据
#             print(strline)
        return None
    return True

class LangageObj():
    def __init__(self, xlsObj, encodingMap, AppMap=None):
        self.xls = xlsObj
        self.keymap = encodingMap  # 获取 编码格式对应表
        self.appmap = AppMap  # 获取要生成文件的对应表
        self.delmap = []  # 不同平台需要排除的字段表
        self.encodType = 'utf-8'  # 当前语言的编码格式
        self.curFileName = ''  # 当前语言的文件名字
        self.curFileObj = None  # 生成当前文件的操作句柄
        self.key = ''  # 当前语言的  key 值
        self.col = 65  # 程序运行实时列数 （A）
        self.row = 0  # 程序运行实时行数
        self.curline = ''  # 当前行
        self.hint = ''  # 全局提示
        self.dest = ''  # 目标生成目标路径
        self.subdir = 'lang'  # 小写  key 语言的存放路径前缀
        self.wordMap = {}
        self.cloMap = {}
        self.keyOrder = ''
        self.buildKeysTable(self.keymap)  # 初始化表



    def xprint(self):
        if len(self.hint) != 0:
            print('\t\t', self.hint)

    def buildKeysTable(self, keyMap, sheetIndex=0):
        iCnt = 65
        for icol in excelPack.getAllColsBySheetIndex(sheetIndex, self.xls):
            if self.getColDetail(icol, keyMap) is True:
                self.wordMap[self.key] = icol  # 排除前两行信息行
                self.cloMap[self.key] = iCnt
                self.keyOrder += self.key
            else:
                self.xprint()
            iCnt += 1
            self.col = iCnt
        print('self.keyOrder = ', self.keyOrder)

    def GetCloNunBykey(self, key):
        if key in self.wordMap:
            return self.cloMap[key]
        else:
            return False

        # 通过 key 值获取对应列
    def GetColByKey(self, key):
        if key in self.wordMap:
            return self.wordMap[key]
        else:
            return False
    # 检查一列数据是否是有效数据,如果是获得 对于的key值，与文件名
    def getColDetail(self, cloObj, keyMap):
        # 检查键值有效性
        Error = None
        try:
            key = cloObj[10][0]
            if key not in keyMap:
                self.hint = ('\t *** Warning col:%c  Discover a empty col ! ****') \
                % (chr(self.col))
                return Error
            self.key = key
            return True

        except (IndexError, TypeError):  # 无效列处理
            self.hint = ('\t *** Warning col:%c  Discover a empty col ! ****')\
             % (chr(self.col))
            return Error

    #
    def checkAndEncodingOneLine(self, aline):
        if isinstance(aline, str):
            aline = aline.strip(string.whitespace)
        else:
            self.hint = '*** Error 【%c:%04d】  Format error  【%d】 ***' \
            % (chr(self.col), self.row, aline)
            return False

        schLine = self.wordMap['S'][self.row - 1]  # 获取对应的中文列
        self.hint = ''
        if checkFormat(aline, self.key) is True:
#             print("->>> ", aline)

            if schLine in self.delmap:  # 排除 Map 中的项
                self.hint = '\t### Warning 【%c:%04d】   exclude 【%s】 ###'\
                 % (chr(self.col), self.row, aline)
                return False

            # 字符串有效
            line = aline + os.linesep
            try:
                return  line.encode(self.encodType)  # 把 utf-8 格式转化成指定编码
            except UnicodeEncodeError:
                self.hint = '*** Error 【%c:%04d】  Coding %s 【%s】 ***' % (chr(self.col), self.row, self.encodType, aline)
                return False

        elif self.appmap is not None:
            if schLine in self.appmap:  # 生成路径控制数据不做处理
                return False
        elif len(schLine) == 0 :  # 忽略无效行
            return False
        elif not checkFormat(schLine, 'S') :  # 排除中文无效项目对应的项
            return False
        else:
            self.hint = '*** Error 【%c:%04d】  Format error  【%s】 ***' \
            % (chr(self.col), self.row, aline)
            return False

    def upDadeFileObj(self, inString):
        cell = inString.strip(string.whitespace)
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

    # 通过一列数据生成对应的语言文件
    def buildOneCol(self, key, keys=None):
        if keys is None:
            keys = self.keymap

        if key not in keys:
            return None

        self.key = key
        self.encodType = self.keymap[key]
        self.curFileName = 'LANGUAGE.' + self.key

        print('\n\t Building a valid  col: %c  enconde:【%s】   LANGUAGE.%s'\
               % (chr(self.cloMap[self.key]), self.encodType, self.key))

        if self.appmap is None:
            # 组装文件名
            finalPath = ''
            if self.key in string.ascii_lowercase:  # 小写key要添加 sub_dir 路径
                finalPath = os.path.join(self.dest, self.subdir)
            else:
                finalPath = os.path.join(self.dest)

            if not os.path.exists(finalPath):
                os.makedirs(finalPath)
            finalName = os.path.join(finalPath, self.curFileName)
#             print('\n\t Destfile: ', finalName)
            self.curFileObj = open(finalName, 'bw')

        self.row = 0
        for aline in self.wordMap[key]:
            self.row += 1

            if self.appmap is not None:
                self.upDadeFileObj(self.wordMap['S'][self.row - 1])  # 通过中文列 获取需要生成文件的目标

            try:
                retVal = self.checkAndEncodingOneLine(aline)
                if retVal :
                    self.curFileObj.write(retVal)
#                         print('\t\t>> ', aline)
                else:
                    self.xprint();
            #
            except AttributeError :  # 忽略文件第一次中文列表，一开始内容  不在  self.appmap 的情况
                continue

        if self.appmap is None:
            self.curFileObj.close()
        self.row = 0

    # 检查一列数据的有效性，并把有问题的数据打印出来
    def checkOneCol(self, key, keys=None):
        if keys is None:
            keys = self.keymap

        if key not in keys:
            return None

        self.key = key
        self.encodType = self.keymap[key]
        self.curFileName = 'LANGUAGE.' + self.key

        print('\n\t Checking a valid  col: %c  enconde:【%s】   LANGUAGE.%s'\
               % (chr(self.cloMap[self.key]), self.encodType, self.key))
        self.row = 0
        for aline in self.wordMap[key]:
            self.row = self.row + 1
            if self.appmap is not None:
                if self.wordMap['S'][self.row - 1] in self.appmap:
                    continue
            if self.checkAndEncodingOneLine(aline) :
                pass
            else:
                self.xprint();
        self.row = 0

    def ProcOneExcelFile(self, how, keys=None, destpath=None, ExclueMap=[], sheetIndex=0):
        self.dest = destpath
        self.delmap = ExclueMap
        print("\n %s excelfile: %s =========  \n### Dest= %s" % (how, self.xls, self.dest))
        for key in self.keyOrder:
            if how == 'Build':
                self.buildOneCol(key, keys)
            elif how == 'Check':
                self.checkOneCol(key, keys)
            else:
                print(' *** Error ProcOneExcelFile:  unknow  proc cmd [%s]  *** ' % (how))
                return

def buildSheets(xlss):
    for fileName in xlss:
        xobj = LangageObj(fileName, Rules.CodeingMap, Rules.AppMap)
        xobj.ProcOneExcelFile('Check', Rules.CodeingMap)

def main():
    # 获取当前路径下 所有 Excel 表集合
    xlss = [xls for xls in os.listdir(path='.') if xls.endswith('.xls')]
    buildSheets(xlss)
    print('done...')

if __name__ == '__main__':
    main()

#     testCmp()
    pass
