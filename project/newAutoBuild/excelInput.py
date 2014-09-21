'''
Created on 2013年10月12日

@author: Administrator
'''

from fileDetals import OutPutFileDetails
import copy
import excelPack
import os
import re
import shutil
import string
import tarfile
from ctypes import *


# line = 'Simple chinese::GB2312'
#
# print(line[line.rfind('::') + 2:].strip(string.whitespace).lower())

Desktop = os.path.join(os.path.expanduser('~') , 'Desktop')

class ExcleInput():
    '''
        该类主要功能对excle的内容进行读取以及经解析表中的控制字段
    '''
    PCheckFormat = re.compile(r'''
                ^((?=[A-Za-z])|\[(?P<platform>\w+)\]) # 匹配不同平台字段
                (?P<key>[A-Za-z])    # 匹配键值
                /_(?P<num>\d+)_=      # 匹配中间字符
                (?P<value>.*)         # 匹配字段值
            ''', re.X)
    FormatErrorType = {
      'pass':(True, ''),
      'empty':(False, '暂未翻译'),
      'format':(False, '格式错误'),
      'indexError':(False, '编号错误'),
      'blank':(True, '连续空白'),
      'comment':(False, '注释字段')
      }

    key2Name = {
            'S':'简体中文',
            'E':'英文',
            'T':'繁体中文',
            'P':'葡萄牙语',
            'a':'西班牙语',
            'I':'印尼语',
            'R':'俄语',
            'F':'法语',
            'B':'阿拉伯语',
            'G':'德语',
            't':'土耳其语',
            'L':'泰语',
            'H':'希伯来语',
            'V':'越南语',
            'A':'波斯语',
            'i':'意大利语',
            'K':'韩语',
            'C':'捷克语',
            'D':'荷兰语',
            'Y':'斯洛伐克',
            'm':'蒙古语',
            'M':'马来语',
            'Z':'捷克语',
            }

    def __init__(self, xls, keys = 'SEBaLITtFGHVRPA', msgHandle = None):
        '''
        构造函数，输入 Excle 表中的数据
        '''
        self.tables = []
        self.curCol = 1
        self.curIndex = 1
        self.fileCnt = 0
        self.xlsName = os.path.basename(xls)
        self.dest = os.path.join(Desktop, 'objs')
        self.colNameOrder = ''  # 表中有效列的顺序
        self.keyNameOrder = ''  # 表中有效列key的顺序
        self.curPlatformName = ''
        self.tarObj = None
        self.outKeys = keys
        self.errMap = {}
        self.msgHandle = msgHandle
        self.buildKeysTable(excelPack.getAllColsBySheetIndex(0, xls))
        self.difMap = ExcleInput.GetSpecialMap(self.getColBykey('S'))




    def buildKeysTable(self, excleCols):
        """
        构造 self.tables，有效列的数据
        初始化 self.colNameOrder、self.keyNameOrder
        """
        base = ord('A')
        for iCnt, iCol in enumerate(excleCols):
            key = ExcleInput.CheckOneCol(iCol)
            if key:
                iCol.insert(0, chr(iCnt + base))
                self.tables.append(iCol)
                self.colNameOrder += chr(iCnt + base)
                self.keyNameOrder += key
        if 'S' not in self.keyNameOrder:
            if self.msgHandle: self.msgHandle('输入 Eexcl 表检测不到中文行，请检查 Excle 表数据有效性！')

            raise ValueError
        return self.tables

    def buildErrMsgBykey(self, key, check, cellfilter):
        """
         通过 key 检查一列数据的正确性，并添加至错误信息表 self.errMap
        """
        col = self.getColBykey(key)
        schCol = self.getColBykey('S')
        et = self.getEncodeTypeBykey(key)
        fet = ExcleInput.FormatErrorType
        errmesgs = []
        for iCnt, line in enumerate(col):
            emsg = {}
            schLine = schCol[iCnt]
            schCheckret = check(schLine, schLine, 'S')
            if key == 'S':
                checkret = schCheckret
            else:
                checkret = check(line, schLine, key)

            if checkret == fet['indexError']\
            or checkret == fet['empty']:
                emsg['msg'] = "%s\t<=>【%s】" % (line , schLine)
            else:
                emsg['msg'] = line
            emsg['value'] = line
            emsg['hint'] = checkret[1]  # 错误提示信息
            emsg['locate'] = ((col[0], iCnt))

            if  checkret[0] == False and schCheckret[0] == False:
                if cellfilter(schLine) or len(schLine) == 0 :
                    continue
                else:
                    errmesgs.append(copy.deepcopy(emsg))
                    continue
            elif  checkret[0] == False and schCheckret[0] == True:
                errmesgs.append(copy.deepcopy(emsg))
                continue

            try:
                if key == "A" and et.upper() == "CP1256":  # 波斯语特殊处理，不进行编码检查
                        continue

                line.encode(et)  # 把 utf-8 格式转化成指定编码
                continue
            except UnicodeEncodeError:
                emsg['hint'] = '编码出错'
                errmesgs.append(copy.deepcopy(emsg))
                continue

        self.errMap[key] = errmesgs
        return errmesgs


    def getErrMsgByKey(self, key):
        """
        通过  key 获取该语言的错误信息
        """
        if key in self.errMap:
            return self.errMap[key]
        else:
            return self.buildErrMsgBykey(key, ExcleInput.CheckOneCellWithSchCell, ExcleInput.IsSubPathCell)


    def __iter__(self):
        self.curCol = 0
        self.curIndex = 1
        self.fileCnt = 0
        return self

    def __next__(self):

        if self.curCol == len(self.tables):
            raise StopIteration

        curCol = self.tables[self.curCol]  # 当前要操作的行
        schCol = self.getColBykey('S')

        fd = OutPutFileDetails(ExcleInput.GetNextFileDetailByCol(curCol, schCol , self.curIndex))
        if fd.subPath is None:  # 找不到下个文件目标
            raise StopIteration

        else :
            self.curIndex = fd.begin + len(fd.lines)
            self.fileCnt += 1
#             print ("[%2d|%4d:%4d] @ >> %2d : %s " % (self.curCol, fd.begin , fd.begin + len(fd.lines) - 1, self.fileCnt, fd.subPath))
            if self.curIndex >= len(self.tables[self.curCol]):
                self.curIndex = 1
                self.curCol += 1
#                 print("+"*80)
#                 if self.curCol != len(self.tables):
#                     print("next obj is [%s,%4d]" % (self.tables[self.curCol][0], self.curIndex))
#                 else:
#                     print("End of the Excel File...")
            return fd

    def ProcFileInfo(self, fd, doWith = None, subdir = '', specialMap = None):

        key = fd.key
        lines = fd.lines
        begin = fd.begin
        if key != 'S':
            schlines = self.getColBykey('S')[begin: begin + len(lines) ]
        else:
            schlines = lines

        out = copy.deepcopy(fd.lines)
        et = self.getEncodeTypeBykey(key)
        colErrmsg = self.getErrMsgByKey(key)

        subpath = fd.subPath
        if key in string.ascii_lowercase:  # 小写key值需要添加前缀
            subpath = os.path.join(fd.subPath, subdir)
        fname = os.path.join(subpath, 'LANGUAGE.' + key)

        for msg in colErrmsg :
            errRowNum = msg['locate'][1]  # 获取错误字段所在行数
            value = msg['value']
#             print(msg, out[:2])
            end = begin + len(lines)
            if begin <= errRowNum <= end :
#                 print ("-%s-" % (value))
                out.remove(value)
            if errRowNum < 2 and value in out:
                # errRowNum < 2 每列数据第 0 跟第1 保留不做字段显示
                out.remove(value)



        # 去除不同平台要排除的字段
        if specialMap is not None:
            for iCnt, schline in enumerate(schlines):
                # 以中文行为基准
                ret = ExcleInput.IsSpecialPlatformCell(schline)
                if ret :  # 当前文件对象有需要排除的字段
                    platform = ret[0]  # 获取平台信息
                    value = ret[1]  # 提取中文字段值
                    line = lines[iCnt]  # 当前行字段值

                    # 如果 中文字段不在 specialMap 中则可判断该字段需要排除
                    if value not in specialMap:
#                         print("##", line)
                        out.remove(line)  # 在输入缓冲中删除需要排除的字段

                    elif key == 'S':
                        # 如果不需要删除且文件对象为中文则去除字段前的平台信息
                        index = out.index(line)
#                         print('@@', index)
#                         print(out[index])
                        out[index] = value  # 去除不同平台的控制信息
        # 去除空行并转码
        finalout = [line for line in out if len(line) > 0]
        if doWith is None:
            return fname, finalout
        return doWith(fname, finalout)

    @staticmethod
    def PrintFileInfo(fn, lines):
        print('\n' + fn + '+' * (50 - len(lines)))
        for i in lines:
            print (">>", i)
        print('-' * 50)
    def ReportErr(self, printErr = None):

        fet = ExcleInput.FormatErrorType
        if len(self.outKeys) is not 0:
            keys = self.outKeys
        else:
            keys = self.keyNameOrder

        if printErr is None:
            print('\n\n')
            print('=' * 80)
            print('##Begin ReportErr: -*- %s -*-... ' % self.xlsName)
            for key in keys:
                emsgs = self.getErrMsgByKey(key)
                if len(emsgs):
                    for msg in emsgs:
                        if msg['hint'] != fet['comment'][1] and  msg['locate'][1] > 1:
                            print('\t[%s:%3d] *** %s *** %s' \
                                  % (msg['locate'][0], msg['locate'][1], msg['hint'], msg['msg']))
                    print()

            print('=' * 80, end = "\n\n")
        else:
            printErr(None, keys)


    def SaveFile(self, fn, lines):
        key = fn[-1]
        et = self.getEncodeTypeBykey(key)

        absfname = os.path.join(self.dest, self.curPlatformName, fn)

        dirName = os.path.dirname(absfname)
        if not os.path.exists(dirName):
            os.makedirs(dirName)

        with open(absfname, 'wb') as fobj:

            if key == 'A' and et.upper() == 'CP1256':
                # ！ 由于PYTHON 自带转码函数 在转换波斯语 utf-8 --> CP1256 编码的时候会报错，所以使用 Windows 转码API进行转码
                buffers = []
                cbuf = c_buffer(4096)
                for line in lines:
                    windll.kernel32.WideCharToMultiByte(1256, 0, line + os.linesep, -1, cbuf, 4096, 0, 0)
#                     print(cbuf.value)
                    fobj.write(cbuf.value)
            else:
                buffers = [(line + os.linesep).encode(et) for line in lines]
                for buf in buffers:
                        fobj.write(buf)



    def initTarFile(self):
        tarName = self.curPlatformName + '_language.' + self.outKeys + '.tgz'
        tarFile = os.path.join(self.dest, tarName)
        dirName = os.path.dirname(tarFile)
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        self.tarObj = tarfile.open(tarFile, mode = 'w:gz')

    def endTarFile(self):
        if self.tarObj is not None:
            self.tarObj.close()
            self.tarObj = None
        delTextObj = os.path.join(self.dest, self.curPlatformName)

        if os.path.exists(delTextObj):
#             print(delTextObj)
            shutil.rmtree(delTextObj)
    def TarFile(self, fn, lines):
        if self.tarObj is None:
            self.initTarFile()

        key = fn[-1:]
        et = self.getEncodeTypeBykey(key)
        absfname = os.path.join(self.dest, self.curPlatformName, fn)

        dirName = os.path.dirname(absfname)
        if not os.path.exists(dirName):
            os.makedirs(dirName)

        with open(absfname, 'wb') as fobj:
            if key == 'A' and et.upper() == 'CP1256':
                # ！ 由于PYTHON 自带转码函数 在转换波斯语 utf-8 --> CP1256 编码的时候会报错，所以使用 Windows 转码API进行转码
                buffers = []
                cbuf = c_buffer(4096)
                for line in lines:
                    windll.kernel32.WideCharToMultiByte(1256, 0, line + os.linesep, -1, cbuf, 4096, 0, 0)
#                     print(cbuf.value)
                    fobj.write(cbuf.value)
            else:
                buffers = [(line + os.linesep).encode(et) for line in lines]
                for buf in buffers:
                        fobj.write(buf)

        odir = os.path.abspath('.')
        os.chdir(os.path.join(self.dest, self.curPlatformName))
        self.tarObj.add(fn)
        os.chdir(odir)


    def SetPlatformName(self, name):
        self.curPlatformName = name

    def getColBykey(self, key):
        ret = self.keyNameOrder.find(key)
        if ret is not None:
            return self.tables[ret]
        else:
            return False

    @staticmethod
    def GetNextFileDetailByCol(col, schCol = None, index = 0):
        """
        describe:通过 中文列  查找返回 下需要生成文件的信息：
        return：
            subPath: 所要生成文件对象的附加路径
            lines： 所要生成文件对象的 数据
            begin： 第一条数据在 ECXLE表格中的行数
            key: 文件所要生成的key值
        """
        if schCol is None:
            schCol = col

        fileDetail = {'subPath':None,
                      'lines':[],
                      'begin':1,  # 对于没有一行数据只生成一个文件的Excle表数据从第一个开始
                      'key': ExcleInput.CheckOneCol(col),
                      'encodeType':ExcleInput.GetEncodeType(col[1]),
                      }

        leftCells = col[index:]
        leftSchCells = schCol[index:]
        for  iCnt, iCell in enumerate(leftCells):

#             print("\t>>", iCell)
            iSchCell = leftSchCells[iCnt]
            ret = ExcleInput.IsSubPathCell(iSchCell)
            if ret :  # 找到一个有效文件单元格
                if fileDetail['subPath'] is None:
                    fileDetail['subPath'] = ret
                    fileDetail['begin'] = index + iCnt + 1  # 起始文件数据单元格由 找到的第一个有效文件单元格的下一个开始
                    continue
                else:
#                     end = index + iCnt - 1  # 结束文件数据单元格 索引 为找到的第二个有效文件单元格的上一个结束
                    return  fileDetail

            elif fileDetail['subPath'] is not None:
                fileDetail['lines'].append(iCell)  # 普通数据单元格 添加到 lines 中

        if fileDetail['subPath'] is None :
#             print('have no subPath')
            fileDetail['subPath'] = ''
            fileDetail['lines'] = leftCells
            return fileDetail
        elif fileDetail['subPath'] is not None:  # 到达一行的结束
            return fileDetail

    @staticmethod
    def GetEncodeType(cell = 'Simple chinese::GB2312', sep = '::'):
        '''
        获取数据的所要生成文件的编码格式（如果未定义默认返回utf-8）
        要定义一列数据，需要在该列的第一个单元 以  <自定义文字>::<编码格式> 定义编码格式
        例如 在 cells(1,1) 中定义有  [中文::GB2312] 则可认为把改列编码选为 "GB2312"
        '''
        if isinstance(cell, str) and cell.rfind(sep) > 0:
            return cell[cell.rfind(sep) + 2:].strip(string.whitespace).lower()
        return 'utf-8'

    def getEncodeTypeBykey(self, key):
        col = self.getColBykey(key)
        return ExcleInput.GetEncodeType(col[1])


    @staticmethod
    def CheckOneCol(col):
        '''
        检查一列是否是有效数据列，
        如果是有效数据列返回相应key值，如果非有效列返回 False
        
        '''
        keydit = {}
        curmaxkeycnt = 0
        for iCnt in range(2, len(col)):
            try:
                key = col[iCnt][0]
                if key not in string.ascii_letters:
                    continue

                fet = ExcleInput.FormatErrorType
                if fet['pass'] != ExcleInput.CheckFormat(col[iCnt], key):
                    continue

                if key not in keydit:
                    keydit[key] = 1
                else:
                    keydit[key] += 1

            except (IndexError, TypeError):  # 无效列处理
                continue

        finalkey = 'S'
        for key in keydit:
            if keydit[key] > curmaxkeycnt:
                curmaxkeycnt = keydit[key]
                finalkey = key
#         print(keydit)
        if curmaxkeycnt > len(col) * 0.68:
            return finalkey
        else:
            return False

    @staticmethod
    def IsSubPathCell(cell, sep = '@@'):
        '''
        判断单元格是否代表生成文件信息
        定义文件格式 :  <自定义文字>::<生成文件附加路径> 
        例如 在 cells(1,2) 中定义有  [主界面::app\main\language] 
        则可认为该单元格为定义文件格式的单元格，接下来的数据需要出存放到   sys.path.jone(<目标路径>,app\main\language) 中
        '''
        if isinstance(cell, str) and cell.rfind(sep) > 0:
            return cell[cell.rfind(sep) + 2:].strip(string.whitespace)
        else :
            return False

    @staticmethod
    def IsSpecialPlatformCell(cell):
        ret = ExcleInput.PCheckFormat.match(cell)
        if ret:
            detail = ret.groupdict()
#             print(detail['platform'])
            if detail['platform']:
                return detail['platform'], cell[ cell.find(']') + 1:]
            else:
                return False
        else:
            return False
    @staticmethod
    def GetSpecialMap(schCol):
        '''
        检查是否需要区分平台，
        如果需要返回平台区分表 difMap{}，如果非有效行返回 False
        '''
        difMap = {}
        for iCell in schCol:
            ret = ExcleInput.IsSpecialPlatformCell(iCell)
            if ret:
                if ret[0] not in difMap:
                    difMap[ret[0]] = [ret[1]]
                else:
                    difMap[ret[0]].append(ret[1])
        return difMap

    @staticmethod
    def GetCellDetail(cell):
        ret = ExcleInput.PCheckFormat.match(cell)
        if ret:
            ret = ret.groupdict()
        return ret

    @staticmethod
    def CheckFormat(strline, key):

        fet = ExcleInput.FormatErrorType
        if not isinstance(strline, str):
            return fet['format']

        ret = ExcleInput.PCheckFormat.match(strline)

        if ret :
            detail = ret.groupdict()
            if len(detail['value']) == 0:
                return fet['empty']
            if detail['key'] != key:
                return fet['format']
        else:
            if len(strline) == 0:
                return fet['empty']
            elif re.search(r''' \s+''', strline):  # 检查连续空格数据
                return fet['blank']
            elif strline[0] == '#':
                return fet['comment']
            else:
                return fet['format']

        if re.search(r''' \s+''', strline):  # 检查连续空格数据
                return fet['blank']

        return fet['pass']

    @staticmethod
    def CheckOneCellWithSchCell(cell, schcell, key):
        fet = ExcleInput.FormatErrorType
        ret = ExcleInput.CheckFormat(cell, key)

        if  fet['comment'] == ExcleInput.CheckFormat(schcell, 'S'):
            return fet['comment']

        elif fet['pass'] == ret and key != 'S':
            celldetail = ExcleInput.GetCellDetail(cell)
            schcelldetail = ExcleInput.GetCellDetail(schcell)

            if celldetail and schcelldetail:
                if celldetail['num'] != schcelldetail['num']:
                    return fet['indexError']
            return fet['pass']
        else:
            return ret


    def ProcTar(self, keys, dest):
        self.dest = dest
        self.outKeys = keys
        if len(self.difMap) == 0:
            shortname, extendsion = os.path.splitext(self.xlsName)
            self.SetPlatformName(shortname)
            for fd in self:
                if fd.key in keys:
                    self.ProcFileInfo(fd, self.TarFile)
            self.endTarFile()
            return

        for difkey in self.difMap:
            shortname, extendsion = os.path.splitext(self.xlsName)
            platformName = shortname + difkey
            self.SetPlatformName(platformName)

            for fd in self:
                if fd.key in keys:
    #                 print(ei.difMap[difkey])
                    self.ProcFileInfo(fd, self.TarFile, '', self.difMap[difkey])
            self.endTarFile()

    def ProcText(self, keys, dest):
        self.dest = dest
        self.outKeys = keys
        if len(self.difMap) == 0:
            shortname, extendsion = os.path.splitext(self.xlsName)
            self.SetPlatformName(shortname)
            for fd in self:
                if fd.key in keys:
                    self.ProcFileInfo(fd, self.SaveFile, 'lang')
            return

        for difkey in self.difMap:
            shortname, extendsion = os.path.splitext(self.xlsName)
            platformName = shortname + difkey
            self.SetPlatformName(platformName)

            for fd in self:
                if fd.key in keys:
    #                 print(ei.difMap[difkey])
                    self.ProcFileInfo(fd, self.SaveFile, 'lang', self.difMap[difkey])

def OutPutTextFileByKeys(xls, keys):

    ei = ExcleInput(xls, keys)
    if len(ei.difMap) == 0:
        for fd in ei:
            if fd.key in keys:
                ei.ProcFileInfo(fd, ei.SaveFile, 'lang')
        return

    for difkey in ei.difMap:
        shortname, extendsion = os.path.splitext(xls)
        platformName = shortname + difkey
        ei.SetPlatformName(platformName)
        for fd in ei:
            if fd.key in keys:
                ei.ProcFileInfo(fd, ei.SaveFile, 'lang', ei.difMap[difkey])


def OutPutTarFileByKeys(xls, keys):
    ei = ExcleInput(xls, keys)

    ei.ReportErr()
    if len(ei.difMap) == 0:
        for fd in ei:
            if fd.key in keys:
                ei.ProcFileInfo(fd, ei.TarFile)
        ei.endTarFile()
        return

    for difkey in ei.difMap:
        shortname, extendsion = os.path.splitext(xls)
        platformName = shortname + difkey
        ei.SetPlatformName(platformName)

        for fd in ei:
            if fd.key in keys:
#                 print(ei.difMap[difkey])
                ei.ProcFileInfo(fd, ei.TarFile, '', ei.difMap[difkey])
        ei.endTarFile()


if __name__ == "__main__":
#     OutPutTarFileByKeys('NewArch.xls', 'SE')
#     ExcleInput('NewArch.xls').ReportErr()
    print('done...')
