'''
Created on 2013年9月6日

@author: hp41
'''

from autoBuildLanguage import Rules
import excelPack
import os
import string

sub_dir = 'lang\\'
#检查一列数据是否是有效数据
def checkIsGoodCol(cloObj):
    # 检查键值有效性
    try:
        key = cloObj[10][0];
        if key not in Rules.CodeingMap:
            return
    except Exception:   # 无效列处理
        print ('*** Discover a empty row !! ****')
        return
 
 
    
def checkOneLine(aline, key):
    head = key + '/_'
    return aline.startswith(head)
    
endline = os.linesep
def buildOne(cloObj, dest_dir='.\language'):
        key = '0'
        fname = ''

        if not checkIsGoodCol(cloObj):
            return
        
        # 组装文件名
        if key in string.ascii_lowercase:
            fname = sub_dir + 'LANGEUAGE.' + key
        else:
            fname = 'LANGEUAGE.' + key    
        
        # 获取文件编码格式
        ecodeType = Rules.CodeingMap[key]
        print('DestDir:%10s ' % (dest_dir))
        print('DestFileName:%10s  encoding as -- %s -- ' % (fname, ecodeType))
        
        fboj = open(os.path.join(dest_dir, fname), 'bw') 
        rowNun = 0
        for aline in cloObj:
            rowNun = rowNun + 1
            try:
                if checkOneLine(aline.strip(string.whitespace), key):   # 检查文件数据有效性
#                     print(aline)
                    aline = aline + endline
                    coding_bytes = aline.encode(ecodeType)   # 把 utf-8 格式转化成指定编码
                else:
                    print('*** invalid line %3d : [%s]  key=[%s] ***' % (rowNun, aline, key))
                    continue
            except Exception:
                try:
                    print('*** coding %s  row: %3d  %s Error... ***' % (ecodeType, rowNun, aline[0:aline.find('=')]))    
                except Exception:
                    print('*** coding %s  row: %3d  [cant not print string] Error... ***' % (ecodeType, rowNun))
            else:
                fboj.write(coding_bytes)
        fboj.close()
        print('===')    

def buildAll(excelfile='sourceLanguage.xls', dest_dir='.\language', sheetIndex=0):
    for aclo in excelPack.getAllColsBySheetIndex(sheetIndex, excelfile):
        buildOne(aclo, dest_dir)

def buildAllSheet(xlss):
    dest_dir = ''
    for fileName in xlss:
        #生成目标文件夹的名称为 
        dest_dir = 'obj\\' + fileName[0:fileName.find('.xls')]
        if not os.path.exists(os.path.join(dest_dir, sub_dir)):
            os.makedirs(os.path.join(dest_dir, sub_dir))
        print (dest_dir)
        buildAll(fileName, dest_dir)
#         input('Build '+ fileName +' success! press any key to continue....')    

def main():
    xlss = [xls for xls in os.listdir(path='.') if xls.endswith('.xls')]
    buildAllSheet(xlss)
    print('done...')
    
    
if __name__ == '__main__':
    main()
  
  
    
#     try:
#         xlss = [xls for xls in os.listdir(path='.') if xls.endswith('.xls')]
#         buildAllSheet(xlss)
#     except  Exception as e:
#         print('buildAllSheet() Error: %s ' % (e))
#     finally:
#         input('done press any key to continue....')
#         pass
