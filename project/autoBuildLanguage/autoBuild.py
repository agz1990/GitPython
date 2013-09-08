'''
Created on 2013年9月6日

@author: hp41
'''

from autoBuildLanguage import Rules
import excelPack
import os
import string

sub_dir = 'lang\\'
xlsObj = {'xls'       :'None',  # 当前操作的 xls对象
        'key'       :'None',  # 当前语言key值
        'encodType' :'None',  # 当前文件对象编码格式
        'curFile'   :'None',  # 当前文件名称
        'col'       :0,  # 当前操作的行
        'row'       :0,  # 当前操作的列
        'preLine'   :'None',
        'curLine'   :'None',
        'hint'      :''  # 提示信息
        }

def xlsObjPrint(hint):
    if len(hint) != 0:
        print('\t', hint)


# 检查一列数据是否是有效数据
def GetColDetail(cloObj):
    # 检查键值有效性
    Error = None
    try:
        key = 'S'
        key = cloObj[10][0]
#         print(cloObj[10])
        if key in Rules.CodeingMap:
                # 组装文件名
                if key in string.ascii_lowercase:  # 小写key要添加 sub_dir 路径
                    fname = sub_dir + 'LANGEUAGE.' + key
                else:
                    fname = 'LANGEUAGE.' + key
        else:  # 无效Key 值
            xlsObj['hint'] = ('*** Warning col:%2d  Discover a empty col ! ****') % (xlsObj['col'])
            return Error

        xlsObj['key'] = key
        xlsObj['encodType'] = Rules.CodeingMap[key]
        xlsObj['curFile'] = fname
        return True
    except IndexError:  # 无效列处理
        xlsObj['hint'] = ('*** Warning col:%2d  Discover a empty col ! ****') % (xlsObj['col'])
        return Error

def checkAndEncodingOneLine(aline, key, encodeType='utf-8'):
    head = key + '/_'
    aline = aline.strip(string.whitespace)
    Error = None
    if aline.startswith(head) is True:
        line = aline + endline
        try:
            return line.encode(encodeType)  # 把 utf-8 格式转化成指定编码
        except UnicodeEncodeError:
            xlsObj['hint'] = '*** Error 【%c:%04d】  Coding %s 【%s】 ***' % (xlsObj['col'], xlsObj['row'], encodeType, aline[0:aline.find('=')])
            return Error
    elif len(aline) == 0:
        xlsObj['hint'] = ''
        return Error
    else:
        xlsObj['hint'] = '*** Error 【%c:%04d】  Format error  【%s】 ***' % (xlsObj['col'], xlsObj['row'], aline)
        return Error

endline = os.linesep
def buildOne(cloObj, dest_dir='.\language'):

        xlsObj['row'] = 0
        if GetColDetail(cloObj) is None:
            xlsObjPrint(xlsObj['hint']);
            return
        print('\nExcelfile: %s============\n\t Discover a valid  col: %c  key: LANGUAGE.%s\n' % (xlsObj['xls'], xlsObj['col'], xlsObj['key']))

        key = xlsObj['key']
        fname = xlsObj['curFile']
        encodeType = xlsObj['encodType']


        fboj = open(os.path.join(dest_dir, fname), 'bw')
        for aline in cloObj:
            xlsObj['row'] = xlsObj['row'] + 1
            try:  # 检查文件数据有效性
                fboj.write(checkAndEncodingOneLine(aline, key, encodeType))
            except TypeError:
                xlsObjPrint(xlsObj['hint'])
                continue
        xlsObj['row'] = 0
        fboj.close()

def buildOneExcelFile(excelfile='sourceLanguage.xls', dest_dir='.\language', sheetIndex=0):
    xlsObj['xls'] = excelfile
    xlsObj['col'] = 65
    for icol in excelPack.getAllColsBySheetIndex(sheetIndex, excelfile):
        xlsObj['col'] = xlsObj['col'] + 1
        buildOne(icol, dest_dir)
    xlsObj['col'] = 0

def buildSheets(xlss):
    dest_dir = ''
    for fileName in xlss:
        # 生成目标文件夹的名称为
        dest_dir = 'obj\\' + fileName[0:fileName.find('.xls')]
        if not os.path.exists(os.path.join(dest_dir, sub_dir)):
            os.makedirs(os.path.join(dest_dir, sub_dir))
        print (dest_dir)
        buildOneExcelFile(fileName, dest_dir)

def main():
    xlss = [xls for xls in os.listdir(path='.') if xls.endswith('.xls')]
    buildSheets(xlss)
    print('done...')

if __name__ == '__main__':
    main()

