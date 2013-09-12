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
    if re.search(r''' \s+|\s$''', strline):   # 检查连续空格数据
#             print(strline)
        return None
    return True

class LangageObj():
    def __init__(self, xlsObj, encodingMap, \
                 destPath='.', AppMap={'中文':''}, ExclueMap=[]):
        self.xls = xlsObj
        self.keymap = encodingMap   # 获取 编码格式对应表
        self.appmap = AppMap   # 获取要生成文件的对应表
        self.delmap = ExclueMap   # 不同平台需要排除的字段表
        self.encodType = 'utf-8'   # 当前语言的编码格式
        self.curFileName = ''   # 当前语言的文件名字
        self.curFileObj = None   # 生成当前文件的操作句柄
        self.key = ''   # 当前语言的  key 值
        self.col = 65   # 程序运行实时列数 （A）
        self.row = 0   # 程序运行实时行数
        self.preLine = ''   # 上一个有效行
        self.curline = ''   # 当前行
        self.hint = ''   # 全局提示
        self.dest = destPath   # 目标生成目标路径
        self.subdir = 'lang'   # 小写  key 语言的存放路径前缀
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
                self.hint = ('\n\t *** Warning col:%c  Discover a empty col ! ****') \
                % (chr(self.col))
                return Error

            self.key = key
            self.encodType = self.keymap[key]
            self.curFileName = 'LANGUAGE.' + self.key
            return True

        except IndexError:   # 无效列处理
            self.hint = ('\n\t *** Warning col:%c  Discover a empty col ! ****')\
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

        schLine = self.ChieseCol[self.row - 1]   # 获取对应的中文列
        self.hint = ''
        if checkFormat(aline, self.key) is True:
#             print("->>> ", aline)

            if schLine in self.delmap:   # 排除 Map 中的项
                self.hint = '\t### Warning 【%c:%04d】   exclude 【%s】 ###'\
                 % (chr(self.col), self.row, aline)
                return False

            # 字符串有效
            line = aline + os.linesep
            try:
                return  line.encode(self.encodType)   # 把 utf-8 格式转化成指定编码
            except UnicodeEncodeError:
                self.hint = '*** Error 【%c:%04d】  Coding %s 【%s】 ***' % (chr(self.col), self.row, self.encodType, aline)
                return False

        elif schLine in self.appmap:   # 生成路径控制数据不做处理
            return False
        elif len(schLine) == 0 :   # 忽略无效行
            return False
        elif not checkFormat(schLine, 'S') :   # 排除中文无效项目对应的项
            return False
        else:
            self.hint = '*** Error 【%c:%04d】  Format error  【%s】 ***' \
            % (chr(self.col), self.row, aline)
            return False

    def upDadeFileObj(self, aline):
        cell = aline.strip(string.whitespace)
#         print(cell)
        if cell in self.appmap:
            try:
                self.curFileObj.close()   # 关闭前一个文件
#                 print(' ***  Close a file : 【%c:%04d】  *** '%(chr(self.col),self.row))
            except AttributeError:
                pass   # 忽略第一个打开

            # 组装文件名
            if self.key in string.ascii_lowercase:   # 小写key要添加 sub_dir 路径
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
    def buildOneCol(self, cloObj, keys=None):
        self.row = 0
        if self.getColDetail(cloObj) is None:
#                 self.xprint();
            return

        if keys is None:
            keys = self.keymap

        if self.key not in keys:
            return None

        print('\t Building a valid  col: %c  enconde:【%s】   LANGUAGE.%s'\
               % (chr(self.col), self.encodType, self.key))
        for aline in cloObj:
            self.row = self.row + 1
            self.upDadeFileObj(self.ChieseCol[self.row - 1])   # 通过中文列 获取需要生成文件的目标
            try:
                retVal = self.checkAndEncodingOneLine(aline)
                if retVal :
                    self.curFileObj.write(retVal)
#                         print('\t\t>> ', aline)
                else:
                    self.xprint();
            #
            except AttributeError :   # 忽略文件第一次中文列表，一开始内容  不在  self.appmap 的情况
                continue
        self.row = 0

    # 检查一列数据的有效性，并把有问题的数据打印出来
    def checkOneCol(self, cloObj, keys=None):
        self.row = 0
        if self.getColDetail(cloObj) is None:
#                 self.xprint();
            return

        if keys is None:
            keys = self.keymap

        if self.key not in keys:
            return None

        print('\n\t Checking a valid  col: %c  enconde:【%s】   LANGUAGE.%s'\
               % (chr(self.col), self.encodType, self.key))
        for aline in cloObj:
            self.row = self.row + 1
            if self.ChieseCol[self.row - 1] in self.appmap:
                continue
            if self.checkAndEncodingOneLine(aline) :
                pass
            else:
                self.xprint();
        self.row = 0
    def ProcOneExcelFile(self, how, keys=None, sheetIndex=0):
        print("\n %s excelfile: %s =========  \n### Dest= %s" % (how, self.xls, self.dest))
        for icol in excelPack.getAllColsBySheetIndex(sheetIndex, self.xls):
            if how == 'Build':
                self.buildOneCol(icol, keys)
            elif how == 'Check':
                self.checkOneCol(icol, keys)
            else:
                print(' *** Error ProcOneExcelFile:  unknow  proc name [%s]  *** ' % (how))
                return
            
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



    
if __name__ == '__main__':
    main()
    
#     testCmp()
    pass
