'''
Created on 2013年9月26日

@author: hp41
'''
import os
import win32com.client as win32
RANGE = range(3, 8)

class Excle():
    def __init__(self, filename=None):
            self.xlApp = win32.Dispatch('Excel.Application')
            if filename:
                self.filename = filename
                if os.path.exists(self.filename):
                    self.xlBook = self.xlApp.Workbooks.Open(filename)
                else:
                    self.xlBook = self.xlApp.Workbooks.Add()
            else:
                self.xlBook = self.xlApp.Workbooks.Add()
                self.filename = 'Untitle'
    def save(self, newfilename=None):
            if newfilename:
                self.filename = newfilename
            self.xlBook.SaveAs(self.filename)

    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp

    def copySheet(self, before):
        "copy sheet"
        shts = self.xlBook.Worksheets
        shts(1).Copy(None, shts(1))

    def newSheet(self, newSheetName):
        sheet = self.xlBook.Worksheets.Add()
        sheet.Name = newSheetName
        sheet.Activate()

    def activateSheet(self, sheetName):
        self.xlBook.Worksheets(sheetName).Activate()

    def activeSheet(self):
        return self.xlApp.ActiveSheet;

    def getCell(self, row, col, sheet=None):
        "Get value of one cell"
        if sheet:
            sht = self.xlBook.Worksheets(sheet)
        else:
            sht = self.xlApp.ActiveSheet
        return sht.Cells(row, col).Value

    def setCell(self, row, col, value, sheet):
        "set value of one cell"
        if sheet:
            sht = self.xlBook.Worksheets(sheet)
        else:
            sht = self.xlApp.ActiveSheet

        sht.Cells(row, col).Value = value


if __name__ == '__main__':
    xl = Excle('Untitle.xls')
    xl.save()
    print('done...')
    pass
