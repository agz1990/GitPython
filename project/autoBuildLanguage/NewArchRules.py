'''
Created on 2013年9月8日

@author: agz
'''


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

LANGUAGE_S = 'gb2312'
LANGUAGE_E = 'utf-8'  # 'cp1252'
LANGUAGE_T = 'utf-8'  # 'big5'
LANGUAGE_P = 'utf-8'  # 'cp1252'
LANGUAGE_a = 'utf-8'  # 'cp1252'
LANGUAGE_I = 'utf-8'  # 'cp1252'
LANGUAGE_R = 'utf-8'  # 'cp1251'
LANGUAGE_F = 'utf-8'  # 'cp1252'
LANGUAGE_B = 'iso8859_6'
LANGUAGE_G = 'utf-8'  # 'cp1252'
LANGUAGE_t = 'utf-8'  # 'cp1254'
LANGUGAE_L = 'utf-8'
LANGUAGE_H = 'utf-8'
LANGUAGE_V = 'utf-8'
LANGUAGE_A = 'iso8859_6'

# 工程路径配置:
DESK_DIR = ''  # 当前系统桌面路径
DEST_DIR = 'obj'  # 生成目标路径
SUB_DIR = 'lang'  # 相对于 ‘DEST_DIR’ 小写语言的目标路径

ValidKeys = None  # 要生成的语言 None 默认生成所有语言

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
            'A':LANGUAGE_A,
            }


AppMap = {
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

ExclueMap35 = [
             'S/_16_=向右键切换输入法，向左键表示删除键',
             'S/_100_=向左键',
             'S/_101_=向右键',

           ]
ExclueMap30 = [
             'S/_16_=*键切换输入法,#键输入空格',
             'S/_100_=*',
             'S/_101_=#',
             ]

def main():
    for key in CodeingMap:
        print('LANGUAGE.%s -------------------- [%s]' \
              % (key, CodeingMap[key].center(12, '-')))
if __name__ == '__main__':
    main()

if __name__ == '__main__':
    pass
