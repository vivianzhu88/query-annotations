from openpyxl import load_workbook
import openpyxl

class RawData():
#object for each RID and Rterms Excel file
    def __init__(self, fN, itemName):
        self.fN = fN
        self.itemName = itemName
        self.workbook = load_workbook(filename=fN)
        self.sheet = self.workbook.active
        self.rDict = {}
        self.sortedKeys = []

    def dictOfterms(self):
    #create dictionary where key is the RadLex item, values are the filepaths
        for row in self.sheet.iter_rows(min_row=2, values_only=True):
            filepath, radlex = row
            rs = radlex.split(", ")
            for r in rs:
                if r in self.rDict:
                    self.rDict[r].append(filepath)
                else:
                    self.rDict[r] = [filepath]
    
    def sortByLen(self):
    #sort by number
        self.sortedKeys = sorted(self.rDict, key=lambda k: len(self.rDict[k]), reverse=True)
    
    def writeResults(self):
    #frequencies of all RadLex items sorted in order of most to least frequent
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.cell(row=1, column=1, value=self.itemName)
        sheet.cell(row=1, column=2, value="Count")
        sheet.cell(row=1, column=3, value="File Paths")
        
        row = 2
        for k in self.sortedKeys:
            sheet.cell(row=row, column=1, value=k)
            sheet.cell(row=row, column=2, value=len(self.rDict[k]))
            sheet.cell(row=row, column=3, value=', '.join(self.rDict[k]))
            row += 1
    
        fN = "freq_" + self.itemName + ".xlsx"
        workbook.save(filename=fN)
    
    def analyze(self):
    #call all the necessary methods in order
        self.dictOfterms()
        self.sortByLen()
        self.writeResults()
    

IDs = RawData("filepath_and_RIDs.xlsx", "RIDs")
IDs.analyze()
Rterms = RawData("filepath_and_Rterms.xlsx", "Rterms")
Rterms.analyze()
