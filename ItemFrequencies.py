from openpyxl import load_workbook
import openpyxl
import json
import pandas as pd
import csv

class RawData():
    #process both ID and Term files
    def __init__(self, fN, fN2):
        self.fN = fN #ID file
        self.fN2 = fN2 #term file
        self.rDict = {}
        self.countDict = {}
        self.sortedKeys = []

    def dictOfterms(self):
    #create dictionary of ID + terms, another dictionary of ID + filepaths
        c = 0
        with open(self.fN) as file1, open(self.fN2) as file2:
            for x, y in zip(file1,file2):
                if c == 0: #skip header line
                    c = 1
                else:
                    #clean csv
                    x = x.rstrip()
                    xx = x.split(",",1)
                    filepath = xx[0]
                    rids = xx[1]
                    if '"' in rids:
                        rids = rids[1:-1]
                    rids = rids.split(" | ")
                    
                    y = y.rstrip()
                    yy = y.split(",",1)
                    filepath = yy[0]
                    rterms = yy[1]
                    if '"' in rterms:
                        rterms = rterms[1:-1]
                    rterms = rterms.split(" | ")
                    
                    #update dict of ID + terms
                    d = dict(zip(rids, rterms))
                    self.rDict = {**self.rDict, **d}
                    
                    #update dict of ID + filepaths
                    for r in rids:
                        if r in self.countDict.keys():
                            self.countDict[r].append(filepath)
                        else:
                            self.countDict[r] = [filepath]
    
    def sortByLen(self):
    #sort IDs by number of filepaths
        self.sortedKeys = sorted(self.countDict, key=lambda k: len(self.countDict[k]), reverse=True)
    
    def writeResults(self):
    #write IDs/terms to JSON and CSV in decreasing frequency
        output = []
        
        #to JSON
        c = 0
        
        for k in self.sortedKeys:
            d = {}
            d["NIDs"] = k
            d["Nterms"] = self.rDict[k]
            d["Count"] = len(self.countDict[k])
            d["File Paths"] = ' | '.join(self.countDict[k])
            output.append(d)
            c += 1
        
        with open("freq.json", "w") as outfile:
            json.dump(output, outfile)
    
        #to CSV
        df = pd.read_json (r"freq.json")
        df.to_csv (r"freq.csv", index = None)
    
    def analyze(self):
    #call all the necessary methods in order
        self.dictOfterms()
        self.sortByLen()

f1 = "filepath_and_NIDs.csv"
f2 = "filepath_and_Nterms.csv"
data = RawData(f1, f2)
data.analyze()
data.writeResults()
