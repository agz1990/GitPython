'''
Created on 2013年9月6日

@author: hp41
'''
import excelPack
import os
import string

# 英语、法语、西班牙语、葡萄牙语、德语、意大利语        西欧Windows
# 俄语                                                                                       西里尔文Windows
# 阿拉伯语                                                                                 ASMO708
# 中文                                                                                        简体中文（GB2312）    
# 繁体中文                                                                                 繁体中文（Big5）    
# 泰文                                                                                        泰文Windows
# 越南语                                                                                    越南文Windows
# 印尼语                                                                                    西欧Windows
# 土耳其语                                                                                土耳其文Windows
# 波斯语                                                                                    阿拉伯文Windows

LANGUAGE_S='gb2312'
LANGUAGE_E='cp1252'
LANGUAGE_T='big5'
LANGUAGE_P='cp1252'
LANGUAGE_a='cp1252'
LANGUAGE_I='cp1252'
LANGUAGE_R='cp1251'
LANGUAGE_F='cp1252'
LANGUAGE_B='iso8859_6'
LANGUAGE_G='cp1252'
LANGUAGE_t='cp1254'


CodeingMap={
            'S':LANGUAGE_S,
            'E':LANGUAGE_E,
            'T':LANGUAGE_T,
            'P':LANGUAGE_P,
            'a':LANGUAGE_a,
            'I':LANGUAGE_I,
            'R':LANGUAGE_R,
            'F':LANGUAGE_F,
            'B':LANGUAGE_B,
            'G':LANGUAGE_G,
            't':LANGUAGE_t,
            }

# dest_dir=r'D:\work folder\tftp_share_point\objs'
sub_dir='lang\\'

def checkOneLine(aline,key):
    head = key+ '/_'
    return aline.startswith(head)
    
    
endline = os.linesep
def buildOne(cloObj,dest_dir='.\language'):
        key='0'
        fname=''
        
        #检查键值有效性
        try:
            key = cloObj[10][0]
            if key not in CodeingMap:
                return
        except Exception: #无效列处理
            print ('*** Discover a empty row !! ****')
            return
        
        #组装文件名
        if key in string.ascii_lowercase:
            fname=sub_dir+'LANGEUAGE.'+ key
        else:
            fname='LANGEUAGE.'+ key    
        
        #获取文件编码格式
        ecodeType=CodeingMap[key]
        print('DestDir:%10s '%(dest_dir))
        print('DestFileName:%10s  encoding as -- %s -- '%(fname,ecodeType))
        
        fboj = open(os.path.join(dest_dir,fname),'bw') 
        rowNun = 0
        for aline in cloObj:
            rowNun = rowNun+1
            try:
                if checkOneLine(aline.strip(string.whitespace),key) == True: #检查文件数据有效性
#                     print(aline)
                    aline = aline + endline
                    coding_bytes=aline.encode(ecodeType)    #把 utf-8 格式转化成指定编码
                else:
                    print('*** invalid line %3d : [%s]  key=[%s] ***'%(rowNun,aline,key))
                    continue
            except Exception:
                try:
                    print('*** coding %s  row: %3d  %s Error... ***'%(ecodeType,rowNun,aline[0:aline.find('=')]))    
                except Exception:
                    print('*** coding %s  row: %3d  [cant not print string] Error... ***'%(ecodeType,rowNun))
            else:
                fboj.write(coding_bytes)
        fboj.close()
        print('\n\n')    

def buildAll(excelfile='sourceLanguage.xls',dest_dir='.\language',sheetIndex=0):
    for aclo in excelPack.getAllColsBySheetIndex(sheetIndex,excelfile):
        buildOne(aclo,dest_dir)

def buildAllSheet(xlss):
    dest_dir=''
    for f in xlss:
        dest_dir='obj\\'+ f[0:f.find('.xls')]
        if os.path.exists(dest_dir) == False:
            os.mkdir(dest_dir)
            os.mkdir(os.path.join(dest_dir,sub_dir))
        print (dest_dir)
        buildAll(f,dest_dir)


if __name__ == '__main__':
    
    try:
        xlss=[xls for xls in os.listdir(path='.') if xls.endswith('.xls')]
        buildAllSheet(xlss)
        input('Build %d success! press any key to continue....',xlss)
    except  Exception as e:
        print('buildAllSheet() Error: %s '%(e))
        input('Error press any key to continue....')
    finally:
        pass

