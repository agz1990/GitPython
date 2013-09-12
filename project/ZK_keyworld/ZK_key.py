'''
Created on 2013年9月12日

@author: agz
'''
from autoBuildLanguage import excelPack

class ZK_key(object):
    '''
    classdocs
    '''

    def __init__(self, xlsObj, keyMap):
        '''
        Constructor
        '''
        self.xls = xlsObj
        self.key = 'S'
        self.hint = ''
        self.col = 65
        self.wordMap = {}
        self.buildKeysTable(keyMap)

    def buildKeysTable(self, keyMap, sheetIndex=0):
        for icol in excelPack.getAllColsBySheetIndex(sheetIndex, self.xls):
            self.col += 1
            if self.getColDetail(icol, keyMap) is True:
                self.wordMap[self.key] = icol  # 排除前两行信息行

    def GetKeyValue(self, key, rootWord, rootKey='S'):
        if rootWord in self.wordMap[rootKey]:
            iCont = 0
            for iRoot in self.wordMap[rootKey]:
                if rootWord == iRoot:
                    return (iCont, self.wordMap[key][iCont ])
                iCont += 1
        # 没有对应关键字
        return None

    # 检查一列数据是否是有效数据,如果是获得 对于的key值，与文件名
    def getColDetail(self, cloObj, keyMap):

        # 检查键值有效性
        try:
            key = cloObj[0][-2]
            if key not in keyMap:
                self.hint = ('\n\t *** Warning col:%c  Discover a empty col ! ****') \
                % (chr(self.col))
                return False
            self.key = key
            return True

        except IndexError:  # 无效列处理
            self.hint = ('\n\t *** Warning col:%c  Discover a empty col ! ****')\
             % (chr(self.col))
            return False

def main():
    keyObj = ZK_key('ZK_keyWords.xls', 'SE')
    print(keyObj.wordMap)
    ret = keyObj.GetKeyValue('E', '工号')
    if ret != None:
        print(ret)
    pass

if __name__ == '__main__':
    main()
    print('done...')
