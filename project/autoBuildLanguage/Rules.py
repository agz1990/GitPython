'''
Created on 2013年9月6日

@author: hp41
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

#工程路径配置:
DESK_DIR = '' # 当前系统桌面路径
DEST_DIR = 'obj' # 生成目标路径
SUB_DIR  = 'lang' # 相对于 ‘DEST_DIR’ 小写语言的目标路径 



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
            }


if __name__ == '__main__':
    pass