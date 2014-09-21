'''
Created on 2013年10月12日

@author: Administrator
'''
import string
import sys

class errorDetaile():
    def __init__(self, type, col, row):
        pass

class Language(object):
    '''
    classdocs
    '''
    def __init__(self, ei):
        '''
        Constructor
        '''
        self.dest = '.'  # 目标生成目标路径
        self.subdir = 'lang'  # 小写  key 语言的存放路径前缀
        self.ei = ei




