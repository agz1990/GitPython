'''
Created on 2013年9月6日

@author: hp41
'''
import Language as LOBJ
import os.path

LANGUAGE_S = 'gb2312'
LANGUAGE_E = 'cp1252'
LANGUAGE_T = 'big5'
LANGUAGE_P = 'cp1252'
LANGUAGE_a = 'cp1252'
LANGUAGE_I = 'cp1252'
LANGUAGE_R = 'cp1251'
LANGUAGE_F = 'cp1252'
LANGUAGE_B = 'iso8859_6'
LANGUAGE_G = 'cp1252'
LANGUAGE_t = 'cp1254'
LANGUGAE_L = 'utf-8'
LANGUAGE_H = 'utf-8'
LANGUAGE_V = 'utf-8'
LANGUAGE_A = 'iso8859_6'


# 工程路径配置:
DESK_DIR = r'C:\Users\hp41\Desktop'   # 当前系统桌面路径

XLS_PATH = r'C:\Users\hp41\Desktop\res'

CodeingMap = {
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
            'L':LANGUGAE_L,
            'H':LANGUAGE_H,
            'V':LANGUAGE_V,
#             'A':LANGUAGE_A,
            }

def buildSheets(in_path, xlss, out_path, keys):
    for fileName in xlss:
        
        fileName = os.path.join(in_path, fileName)
        print(fileName)
        xobj = LOBJ.LangageObj(fileName, CodeingMap)
        dest_obj = os.path.join(out_path, os.path.basename(fileName)[:-4])   # 生成目标路径
        print(dest_obj)
        xobj.ProcOneExcelFile('Check', keys, dest_obj)

def build_language(xlsPath, out_path, keys):
    # 获取当前路径下 所有 Excel 表集合
    xlss = [xls for xls in os.listdir(xlsPath) if xls.endswith('.xls')]
    buildSheets(xlsPath, xlss, out_path, keys)
    print('done...')

if __name__ == '__main__':
    build_language(XLS_PATH, XLS_PATH, CodeingMap)
