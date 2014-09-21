'''
Created on 2013年10月13日

@author: Administrator
'''
import string
import sys

class OutPutFileDetails(object):
    '''
    classdocs
    '''
    def __init__(self, fd):
        '''
        Constructor
        '''
        self.subPath = '',
        self.lines = []
        self.begin = 0
        self.key = ''
        self.encodeType = ''
        self.curCol = []
        self.schCol = []
        self.difMap = {}
        self.dict = fd
        self.initByDit(self.dict)

    def initByDit(self, fd):
        self.subPath = fd['subPath']
        self.lines = fd['lines']
        self.begin = fd['begin']
        self.key = fd['key']
        self.encodeType = fd['encodeType']


    @staticmethod
    def TripLines(lines, schLine):
        pass

    def getFilenameAndBytesBuffer(self):
        if self.key  in string.ascii_lowercase:
            subpath = sys.path.join(self.subPath, 'lang')
        fname = sys.path.join(subpath, 'LANGUAGE.' + self.key)
        bytesBuff = self.lines2BytesBuff()
        return fname, bytesBuff

    def lines2BytesBuff(self):
        iCnt = 0
        lines = self.lines
        schLine = self.schCol
        et = self.encodeType
        langs = OutPutFileDetails.TripLines(lines, schLine)

        try:
            for line in enumerate(langs):
                line.encode(et)  # 把 utf-8 格式转化成指定编码

        except UnicodeEncodeError:
            colVal = self.curCol
            rowVal = iCnt + self.begin
            print('*** Error 【%c:%04d】  Coding %s 【%s】 ***' % colVal, rowVal, et, self.lines[iCnt])
        pass
