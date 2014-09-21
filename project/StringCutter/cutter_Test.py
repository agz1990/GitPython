import cutter
from StringCutter.cutter import DataRange
from rules import Rules

import excelPack
import unittest

xls = 'NewArch.xls';
oneColFileCnt = 27  # 每列可生成27个文件
xlsTableOrder = 'SEBaLITtFGHVRPA'  # 表格中有效列key的顺序
xlsColOrder = 'ADFGHIJKLMNOPQR'  # 表格中有效列头的顺序
outPutFileNum = oneColFileCnt * len(xlsTableOrder)  # 整个表格可生成的文件数
xlsCols = excelPack.getAllColsBySheetIndex(0, xls)

class Test_Rlues(unittest.TestCase):
    def test_reMach(self):
        msg = """
===        
RegExp:%s        
Text:%s
NOT MACH ===
                """
        lanRules = Rules()
        Format = lanRules.get('Format', 'pattern')
#         print(lanRules.get('Filter', 'pattern'))
        Filter = lanRules['Filter']['pattern']
        Blank = lanRules['Blank']['pattern']
        print(Blank)
        testSamples = [
                        # [resault,regExp,Text,re.report]
                        [True, r'hello', 'hello world!'],
                        [True, Format, 'E\tE/_1_=English\tS/_1_=简体中文'],
                        [False, Format, 'E\tE/_2_=English\tS/_1_=简体中文'],
                        [True, Format, 'F\tF/_16_=la touche # pour entrer espace\tS/_16_=#键输入空格\t35'],

                        [True, Filter, 'E\t#E/_1_=English\tS/_1_=简体中文'],
                        [True, Filter, 'E\tE/_1_=English\t#S/_1_=简体中文'],
                        [True, Filter, 'E\tE/_1_=English\tS/1_=简体中文'],  # 基准字段格式检测错误，也会排除
                        [True, Filter, 'G\tF/_16_=la touche # pour entrer espace\tS/_1k6_=#键输入空格    35'],
                        [True, Blank, 'E/_1_=Eng   lish'],
                     ]

        for mustRet, regExp, text in testSamples:
            resault = Rules().Test(regExp, text)
            emsg = msg % (regExp, text)
            self.assertEqual(resault, mustRet, emsg)
        pass




if __name__ == "__main__":
    import sys
    sys.argv = ['', '-v']
    unittest.main()
