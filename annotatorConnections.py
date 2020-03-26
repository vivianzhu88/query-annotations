import urllib.request, urllib.error, urllib.parse
import json
import os
import openpyxl
from pprint import pprint

REST_URL = "http://data.bioontology.org"
ONT = "&ontologies=RADLEX"
API_KEY = ""

def get_json(url):
#get annotations
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def mapRIDs(annotations, get_class=True):
#take annotations and map to Excel spreadsheet of labels and corresponding RIDs
    annDict = {}
    
    #iterate through annotations
    for result in annotations:
        class_details = result["annotatedClass"]
        if get_class:
            try:
                class_details = get_json(result["annotatedClass"]["links"]["self"])
            except urllib.error.HTTPError:
                print(f"Error retrieving {result['annotatedClass']['@id']}")
                continue
        
        #get each RIDs correlating with text
        id = class_details["@id"]
        RID = id[22:]
        for annotation in result["annotations"]:
            label = annotation["text"]
        
        #map all RIDs corresponding to a text into a label
        if label in annDict:
            annDict[label].append(RID)
        else:
            annDict[label] = [RID]

    #put data into to Excel spreadsheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    row = 1
    for key,values in annDict.items():
        sheet.cell(row=row, column=1, value=key)
        sheet.cell(row=row, column=2, value=', '.join(values))
        row += 1

    workbook.save(filename="labels+RIDs.xlsx")

#input for Annotator
text_to_annotate = ("There is a mass on the right lower lobe of the lung.")

#get annotations
annotations = get_json(REST_URL + "/annotator?text=" + urllib.parse.quote(text_to_annotate) + ONT)
mapRIDs(annotations)


