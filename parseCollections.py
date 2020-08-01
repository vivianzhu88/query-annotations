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
import csv

REST_URL = "http://data.bioontology.org"
ONT = "&ontologies=NCIT"
API_KEY = ""
rdict = {}

def createSpreadsheet():
#create csv files
    with open('filepath_and_NIDs.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["File Path", "NIDs"])
        
    with open('filepath_and_Nterms.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["File Path", "Nterms"])
        
    with open('none.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["File Path", "NCIT"])

def toSpreadsheet(f):
#append to csv files
    if f.getRIDs():
        #IDs
        with open('filepath_and_NIDs.csv','a') as csvfile:
            writer=csv.writer(csvfile)
            name = f.getName()
            items = ' | '.join(f.getRIDs())
            writer.writerow([name,items])

        #terms
        with open('filepath_and_Nterms.csv','a') as csvfile:
            writer=csv.writer(csvfile)
            name = f.getName()
            items = ' | '.join(f.getRterms())
            writer.writerow([name,items])

    else:
        #track filenames with no IDs/terms
        with open('none.csv','a') as csvfile:
            writer=csv.writer(csvfile)
            name = f.getName()
            writer.writerow([name,"None"])
    
def check(filename):
    #check if file has already been annotated
    with open('filepath_and_NIDs.csv') as f:
        if filename in [line.split(',')[0] for line in f]:
            return True
            
    with open('none.csv') as f:
        if filename in [line.split(',')[0] for line in f]:
            return True
        
    return False

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
    #return IDs list
        return self.RIDs
    
    def getRterms(self):
    #return terms list
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
            self.text = ' '.join(fullText)
            print(self.text)
        except:
            print(self.filename)
            
    def get_json(self, url):
    #get term json file
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
    #take annotations and make list of RadLex IDs and terms
        for result in annotations:
            class_details = result["annotatedClass"]
            id = result['annotatedClass']['@id']
            rid = id[51:]
            
            #rdict keeps track of IDs and terms already searched
            if rid not in rdict.keys():
                if get_class:
                    while True:
                        try:
                            class_details = self.get_json(result["annotatedClass"]["links"]["self"])
                        except urllib.error.HTTPError:
                            print(f"Error retrieving {result['annotatedClass']['@id']}")
                            time.sleep(5)
                            continue
                        break
                rterm = class_details["prefLabel"]
                rdict[rid] = rterm
            
            else:
                rterm = rdict[rid]
            
            #add to IDs/terms list if unique
            if (rid not in self.RIDs) and (rterm not in self.Rterms) :
                self.RIDs.append(rid)
                self.Rterms.append(rterm)
            
    def getAnnotations(self, name):
    #get annotations from NCBO Annotator
        print(name)
        while not self.exit_flag:
            if not self.work_queue.empty():
                t = self.work_queue.get()
                print(name,"entered")
                while True: #keep trying to send request to URL
                    try:
                        annotations = self.get_json(REST_URL + "/annotator?text=" + urllib.parse.quote(t) + ONT)
                        print(name,"annotated")
                        self.getRadLex(annotations)
                        print(name,"radlex")
          
                    except (ConnectionResetError,urllib.error.HTTPError,TimeoutError): #try requesting again
                        print(name,"too many req")
                        time.sleep(10)
                        continue
                    break
            '''elif self.exit_flag or self.work_queue.empty():
                break'''
        print(name,"exited")
    
    class MyThread (threading.Thread):
    #threads to use when getting annotations from NCBO
        def __init__(self, name, file):
            threading.Thread.__init__(self)
            self.name = name
            self.file = file
        def run(self):
            self.file.getAnnotations(self.name)
    
    def getContents(self):
    #runs all the methods needed to parse files and get annotations
        self.openFile()
        texts = self.split_text() #split text into 500 word pieces
        self.work_queue = queue.Queue(len(texts))
        thread_count = os.cpu_count()
        threads = []
        
        for t in texts:
            self.work_queue.put(t)
        
        for i in range(1,thread_count+1):
            thd = self.MyThread("t"+str(i),self)
            thd.start()
            threads.append(thd)
            
        while not self.work_queue.empty():
            pass

        self.exit_flag = True
        print("done")

        for t in threads:
            t.join()
        print("joined")
        self.done = True

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
#createSpreadsheet()

for f in filesList:
    count +=1
    print(f.getName())
    if not check(f.getName()):
        f.getContents()
        print("content")
        toSpreadsheet(f)
        print("updated")
    else:
        print("already done")
    print(count,"/",len(filesList))
    
end = time.time()
print(end-start)
