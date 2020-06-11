import urllib.request, urllib.error, urllib.parse
import json
import os
import openpyxl
from openpyxl import load_workbook
import time
from pprint import pprint
from socket import error as SocketError
import errno
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import docx
import re
import threading
import queue

REST_URL = "http://data.bioontology.org"
ONT = "&ontologies=RADLEX"
API_KEY = ""

def createSpreadsheet():
#create Excel spreadsheets
    #RIDs
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    
    sheet.cell(row=1, column=1, value="File Path")
    sheet.cell(row=1, column=2, value="RIDs")

    workbook.save(filename="filepath_and_RIDs.xlsx")

    #Rterms
    workbook2 = openpyxl.Workbook()
    sheet = workbook2.active
    
    sheet.cell(row=1, column=1, value="File Path")
    sheet.cell(row=1, column=2, value="Rterms")

    workbook2.save(filename="filepath_and_Rterms.xlsx")

def toSpreadsheet(f):
#put filename and RIDs into to Excel spreadsheet
    #RIDs
    workbook = load_workbook("filepath_and_RIDs.xlsx")
    sheet = workbook.active
    
    if f.getRIDs():
        r = sheet.max_row+1
        sheet.cell(row=r, column=1, value=f.getName())
        sheet.cell(row=r, column=2, value=' | '.join(f.getRIDs()))

    workbook.save(filename="filepath_and_RIDs.xlsx")

    #Rterms
    workbook2 = load_workbook("filepath_and_Rterms.xlsx")
    sheet = workbook2.active
    
    if f.getRIDs():
        r = sheet.max_row+1
        sheet.cell(row=r, column=1, value=f.getName())
        sheet.cell(row=r, column=2, value=' | '.join(f.getRterms()))

    workbook2.save(filename="filepath_and_Rterms.xlsx")

class File():
    def __init__(self, filename):
    #initialize each file
        self.filename = filename
        self.RIDs = []
        self.Rterms = []
        self.text = ""
        self.exit_flag = False
        self.work_queue = None
    
    def getName(self):
    #return filename
        return self.filename[64:]
        
    def getText(self):
    #return text
        return self.text
    
    def getRIDs(self):
    #return RIDs list
        return self.RIDs
    
    def getRterms(self):
    #return Rterms list
        return self.Rterms
    
    def openFile(self):
    #open file and retrieve text
    #has .ore .txt .lsx .ocx .csv .xls .son .xml files
        try:
            with open(self.filename, 'r') as file:
                self.text = file.read()
            return
        except UnicodeDecodeError:
            pass
        
        try:
            df = pd.read_excel(self.filename)
            self.text = df.to_string()
            return
        except:
            pass

        try:
            doc = docx.Document(self.filename)
            fullText = []
            for para in doc.paragraphs:
                txt = para.text.encode('ascii', 'ignore')
                fullText.append(txt)
            self.text = b'\n'.join(fullText)
        except:
            print(self.filename)
            
    def get_json(self, url):
    #get json from annotator
        opener = urllib.request.build_opener()
        opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
        return json.loads(opener.open(url).read())
        
    def split_text(self):
    #split text into 500 word pieces for Annotator to handle

        if len(self.text) > 1:
            txt = re.findall(r"[\w']+", self.text)
            chunks, chunk_size = len(txt), 490
            text = [" ".join(txt[i:i+chunk_size]) for i in range(0, chunks, chunk_size)]
            print(text)
            return text
            
        return [self.text]
        
    def getRadLex(self, annotations, get_class=True):
    #take annotations and makes list of RadLex IDs and terms
        #iterate through annotations
        for result in annotations:
            class_details = result["annotatedClass"]
            if get_class:
                while True:
                    try:
                        class_details = self.get_json(result["annotatedClass"]["links"]["self"])
                    except urllib.error.HTTPError:
                        print(f"Error retrieving {result['annotatedClass']['@id']}")
                        time.sleep(5)
                        continue
                    break

            #get each RIDs + remove duplicates
            id = class_details["@id"]
            rid = id[22:]
            
            if rid not in self.RIDs:
                self.RIDs.append(id[22:])
            
            #get each Rterms + remove duplicates
            rterm = class_details["prefLabel"]
            
            if rterm not in self.Rterms:
                self.Rterms.append(rterm)
        
    def getAnnotations(self):
        while not self.exit_flag:
            if not self.work_queue.empty():
                t = self.work_queue.get()

                while True: #keep trying to send request to URL
                    try:
                        annotations = self.get_json(REST_URL + "/annotator?text=" + urllib.parse.quote(t) + ONT)
                        print("annotated")
                        self.getRadLex(annotations)
                        print("radlex")
          
                    except (ConnectionResetError,urllib.error.HTTPError): #try requesting again
                        print("too many req")
                        time.sleep(10)
                        continue
                    break
                    print("req done")
        print("exited")
    
    class MyThread (threading.Thread):
        def __init__(self, file):
            threading.Thread.__init__(self)
            self.file = file
        def run(self):
            self.file.getAnnotations()
    
    def getContents(self):
    #runs all the methods needed to parse files and get annotations
        self.openFile()
        texts = self.split_text() #split text into 500 word pieces
        self.work_queue = queue.Queue(len(texts))
        thread_count = os.cpu_count()
        threads = []
        
        for i in range(1,thread_count+1):
            thd = self.MyThread(self)
            thd.start()
            threads.append(thd)
        
        for t in texts:
            self.work_queue.put(t)

        while not self.work_queue.empty():
            pass

        self.exit_flag = True
        print("done")

        for t in threads:
            t.join()
        print("joined")

#put all of file paths in Chest_and_Lung_Collections directory into a list
start = time.time()
filesList = []

dir_path = "/Users/vivianzhu/Documents/Annotator/Chest_and_Lung_Collections"
for dp,_,filenames in os.walk(dir_path):
   for f in filenames:
       if f != ".DS_Store":
           f = File(os.path.abspath(os.path.join(dp, f)))
           filesList.append(f)

count = 0
createSpreadsheet()

for f in filesList:
    print(f.getName())
    f.getContents()
    print("content")
    toSpreadsheet(f)
    print("updated")
    
end = time.time()
print(end-start)
    

