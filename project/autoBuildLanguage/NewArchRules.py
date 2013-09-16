'''
Created on 2013年9月8日

@author: agz
'''
import Language as LOBJ
import os.path

# 工程路径配置:
DESK_DIR = r'C:\Users\hp41\Desktop'   # 当前系统桌面路径
# DEST_DIR = r'C:\Users\hp41\Desktop\arm.d'   # 生成目标路径
DEST_DIR = r'D:\work folder\main_code\firmware3.0\trunk\arm'
SUB_DIR = 'lang'   # 相对于 ‘DEST_DIR’ 小写语言的目标路径
DEST_FILE = r'D:\项目\新架构语言项目\自动生成语言包项目\LANGUAGE.xls'   # 生成语言的基准文件
DEST_FILE_OLD = r'D:\项目\新架构语言项目\自动生成语言包项目\LANGUAGE20130909.R0.xls'   # 旧文件 比较用

CodeingMap = {
            'S':'gb2312',
            'E':'utf-8',
            'T':'utf-8',
#             'P':'utf-8',
#             'a':'utf-8',
            'I':'utf-8',
            'R':'utf-8',
            'F':'utf-8',
            'B':'iso8859_6',
            'G':'utf-8',
#             't':LANGUAGE_t,
            'L':'utf-8',
            'H':'iso8859_8',
            'V':'utf-8',
            'A':'utf-8',
            }

ExclueMap35 = [   #    3.5寸屏所需要排除的文件
             'S/_16_=向右键切换输入法，向左键表示删除键',
             'S/_100_=向左键',
             'S/_101_=向右键',
           ]
ExclueMap30 = [   #    3.0寸屏所需要排除的文件
             'S/_16_=*键切换输入法,#键输入空格',
             'S/_100_=*',
             'S/_101_=#',
             ]

AppMap = {   # APP 对应生成路径
        '主界面（main）': r'app\main\language',
        '主菜单（menu）': r'app\mginit\language',
        '用户管理（APP）': r'app\usermng\language',
        '权限管理（APP）': r'app\primng\language',
        '门禁管理（APP）': r'app\access\language',
        'IC卡管理（APP）': r'app\iccardmng\language',
        '通讯设置（APP）': r'app\comset\language',
        '系统设置（APP）': r'app\sysset\language',
        '个性设置（APP)': r'app\myset\language',
        '数据管理（APP）': r'app\datamng\language',
        'U盘管理（APP）': r'app\udiskmng\language',
        '记录查询（APP）': r'app\logquery\language',
        '打印设置（APP）': r'app\printset\language',
        '短消息（APP）': r'app\sms\language',
        '工作号码（APP）': r'app\workcode\language',
        '自动测试（APP）': r'app\autotest\language',
        '系统信息（APP）': r'app\sysinfo\language',
        '公共语言': r'commonres\language',
        '短消息so库（so库）': r'lib\app\libsms\language',
        '用户有效期so库（so库）': r'lib\app\liblawfulday\language',
        '工作号码so库（so库）': r'lib\app\libworkcode\language',
        '验证so库（so库）': r'lib\app\libverify\language',
        '个人记录查询so库（so库）': r'lib\app\librecordquery\language',
        '考勤状态输入so库（so库）': r'lib\app\libattstateinput\language',
        '门禁控制so库（so库）': r'lib\app\libaccesscontrol\language',
        '打印功能so库（so库）': r'lib\app\libprinter\language',
        '用户门禁权限so库（so库）': r'lib\app\libuseraccprivilege\language',
        }

def CmpLanguage(xlsNew, xlsOld, keys):
    xobjNew = LOBJ.LangageObj(xlsNew, CodeingMap)
    xobjOld = LOBJ.LangageObj(xlsOld, CodeingMap)
    for key in keys:
        compareXbojs(xobjOld, xobjNew, key)

# 必须保证中文是不修改的情况下进行对比，默认比较中文
def compareXbojs(xls1, xls2, key='S'):
    iRow = 0
    iCnt = 1
    print('\n\n**************')
    if key in 'ST':
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

    elif key in CodeingMap:   # 简体中文与繁体中文不需要参考
        ChineseCol = xls1.ChieseCol
        keyCol1 = xls1.getRolByKey(key)
        keyCol2 = xls2.getRolByKey(key)
        for iSCH in ChineseCol:
            try:
                if keyCol1[iRow] != keyCol2[iRow]:
                    print('%2d:中文  【%s】   %c:%03d -- 【%s】 < == 原 :【%s】  '\
                          % (iCnt, iSCH, key, iRow, keyCol2[iRow], keyCol1[iRow]))
#                     print('%c%03d\t%s\t%s\t%s'\
#                           % (key, iRow, iSCH, keyCol1[iRow], keyCol2[iRow]))
                    iCnt += 1
            except IndexError:
                print('**************')
                continue
            iRow += 1
    else:
        print('\t *** Warning unknow key[%c] ! ****' % (key))
    print('**************')


    
# 自动生成新架构小彩屏  3.5/3.0 寸语言文件
def build_NewArch(xlsName, keys):
    xobj = LOBJ.LangageObj(xlsName, CodeingMap, AppMap)
    xobj.ProcOneExcelFile('Build', keys, os.path.join(DEST_DIR, 'zmm100_tft35'), ExclueMap35)
    xobj.ProcOneExcelFile('Build', keys, os.path.join(DEST_DIR, 'zmm100_tft3'), ExclueMap30)

def check_NewArch(xlsName, keys=None):
    xobj = LOBJ.LangageObj(xlsName, CodeingMap, AppMap)
    xobj.ProcOneExcelFile('Check', keys)


def main():
    
    while(True):
        print("\n\n")
        print("*"*80)
        print('\t(B)uild :Build New Arch Language obj.')
        print('\t(C)heck:Check language.xls file format.')
        print('\t(H)istory:Show history change.')
        print('\t(Q)uit: exit the console.')
        keys = input("\n>> Please Choose: ")
        
        if keys.lower()[0] == 'q':
            return
        elif keys.lower()[0] == 'c':
            keys = input("--->> Please input the keys you want (C)heck: ")
            if keys.lower() == "all":
                check_NewArch(DEST_FILE)
            else:
                check_NewArch(DEST_FILE, keys)
            continue
        elif keys.lower()[0] == 'b':
            keys = input("--->> Please input the keys you want (B)uild: ")
            if keys.lower() == "all":
                keys = [key for key in CodeingMap]
            build_NewArch(DEST_FILE, keys)
        elif keys.lower()[0] == 'h':
            keys = input("--->> Please input the keys you want show (H)istory: ")
            if keys.lower() == "all":
                keys = [key for key in CodeingMap]
            CmpLanguage(DEST_FILE, DEST_FILE_OLD, keys)
            
if __name__ == '__main__':
    main()
    print ('done...')
