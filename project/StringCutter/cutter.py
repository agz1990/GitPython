
from string import Template
import copy
import excelPack
from rules import Rules


xls = 'NewArch.xls';
oneColFileCnt = 27  # 每列可生成27个文件
xlsTableOrder = 'SEBaLITtFGHVRPA'  # 表格中有效列key的顺序
xlsColOrder = 'ADFGHIJKLMNOPQR'  # 表格中有效列头的顺序
outPutFileNum = oneColFileCnt * len(xlsTableOrder)  # 整个表格可生成的文件数
xlsCols = excelPack.getAllColsBySheetIndex(0, xls)

# cfg = Rules('cutter.ini')
# CheckTextTemplate = Template(cfg['Format']['textFormat'])

# CheckTextTemplate = Template('${key}\t${value}\t${encode}')
class Cell():
    def __init__(self, dict_):
        super(Cell, self).__init__()
        self.Dict2Obj(dict_)

    def Dict2Obj(self, dict_):
        for att in dict_:
            setattr(self, att, dict_[att])

    def Obj2Dict(self):
        _dict = { att:getattr(self, att) for att in dir(self)\
                 if att[0:2] != '__' and not callable(getattr(self, att))}
        return _dict


class DataRange(dict):

    def __init__(self, xlsCols, rules, dict_={}):
        super(DataRange, self).__init__(dict_)
        self.rules = rules
        self.rawdata = xlsCols
        self.baseColNum = ord('A')
        self.ColCnt = len(xlsCols)
        self.buildCells(xlsCols)

    def buildCells(self, Cols):
        cellDict = {'encode': 'UTF-8', 'msg': '', 'value': 'E/_1_=English', 'key': 'S'}
        for iColCnt, iCol in enumerate(Cols, start=ord('A')) :  #

            self[chr(iColCnt)] = iCol
            for iRowCnt, value in enumerate(iCol):
                locade = (chr(iColCnt), iRowCnt)
                cellDict['value'] = copy.deepcopy(value)
                if  0 < iRowCnt < 10 :
                    self[locade] = Cell(copy.deepcopy(cellDict))

    def chekOneCol(self, col):
        pass


    def procRules(self):
        rules = self.rules.getOrder()

        for iCol in self.rawdata:
            colNum = self.chekOneCol(iCol)
            if  not colNum:
                continue

#             for rule in self.rules.getOrder():
#                 pattern = self.rules.get(rule, 'pattern')
#
#                 pass  #



#         for i, locade in enumerate(self):
# #             if i < 10:
#             print(i, locade, self[locade].value)
#
if __name__ == '__main__':
    rules = Rules('cutter.ini')
#     print(rules.sections())
    xls = DataRange(xlsCols, rules)

#     for index in xls:
#         cell = xls[index]
#         info = CheckTextTemplate.safe_substitute(cell.Obj2Dict())
#         print(info)
    print('done...')
