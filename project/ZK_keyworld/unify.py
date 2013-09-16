'''
Created on 2013年9月13日

@author: hp41
'''
from ZK_keyworld.ZK_key import ZK_key
from autoBuildLanguage import Language as LOBJ
from autoBuildLanguage.NewArchRules import CodeingMap
import re
import xlwt3

# 工程路径配置:
DESK_DIR = r'C:\Users\hp41\Desktop'  # 当前系统桌面路径
# DEST_DIR = r'C:\Users\hp41\Desktop\arm.d'   # 生成目标路径
DEST_DIR = r'D:\work folder\main_code\firmware3.0\trunk\arm'
SUB_DIR = 'lang'  # 相对于 ‘DEST_DIR’ 小写语言的目标路径
DEST_FILE = r'D:\项目\新架构语言项目\自动生成语言包项目\LANGUAGE.xls'  # 生成语言的基准文件
kEY_XLS = r'D:\GitHub\GitPython\project\ZK_keyworld\ZK_keyWords.xls'

wbk = xlwt3.Workbook()
sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)

keyReg = re.compile(r'''
                ^(?P<key>[A-Za-z])    # 匹配键值
                /_(?P<num>\d+)_=      # 匹配中间字符
                (?P<value>.+)         # 匹配字段值
                ''', re.X)
def ModifyExcel(x, y, value):
    sheet.write(x, y, value)
    pass

def PrcoUinify(lanObj, keyObj, key):
    lanSchCol = lanObj.GetColByKey('S')
    keySchCol = keyObj.GetColByKey('S')
    iCol = lanObj.GetColByKey(key)

    row = 1
    for oneLine in lanSchCol:
        match = keyReg.match(oneLine)
        if match is not None:
            value = match.groupdict()['value']
            if value in keySchCol:
                keyValue = keyObj.GetKeyValue(key, value, rootKey='S')
                match = keyReg.match(iCol[row - 1])
                lanValue = match.groupdict()['value']
                if  lanValue == keyValue:  # 判断当前行是否与ZK_keywords.xls 表中对应字段相一致
#                     print("\t字段 [%s] 已统一.." % (oneLine))
                    pass
                else:
                    col = lanObj.GetCloNunBykey(key)
                    print("字段 [%s] \t【%c:%03d】 [%s] \t\t key[%s] 未统一.." % (oneLine, chr(col), row, lanValue, keyValue))
                    new_lan = match.expand(r'\g<key>/_\g<num>_=%s' % keyValue)
                    print("\t--【%c:%03d】--  [%s] s==> [%s]" % (chr(col), row, iCol[row - 1], new_lan))
                    ModifyExcel(row - 1, col - 65, new_lan)
        row += 1
    wbk.save('test.xls')


def main():
    lanobj = LOBJ.LangageObj(DEST_FILE, CodeingMap)
    keyobj = ZK_key(kEY_XLS, CodeingMap)
    PrcoUinify(lanobj, keyobj, 'H')

if __name__ == '__main__':
    main()
