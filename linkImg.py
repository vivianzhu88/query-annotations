from xml.dom import minidom
import openpyxl
from openpyxl import load_workbook
import os
from lxml import etree
import json
import csv

filedata =  {}
#link = 'https://www.cancerimagingarchive.net/viewer/?study=' + study + '&series=' + series #useful?

def toCSV(data):
    fields = ["Nodule/NonNodule", "Nodule/NonNodule ID", "Subtlety", "Internal Structure", "Calcification", "Sphericity", "Margin", "Lobulation", "Spiculation", "Texture", "Malignancy", "Confidence", "Obscuration", "Reason", "Image Z Postion", "LIDC ReadMessage UID", "IDRI ReadMessage UID", "SeriesInstanceUID", "StudyInstanceUID", "imageSop_UID", "XY Coordinates"]
    rows = data
    filename = "LIDC-IDRI.csv"
    
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

def checkTag(tag, v=None):
    if tag:
        if v is None:
            return tag[0].firstChild.nodeValue
        else:
            return tag[0].attributes.get("uid").value
    else:
        return ""


def getData(f):
    data = []
    try:
        xml_data = minidom.parse(f)
        print(f)
        
    except (FileNotFoundError, OSError):
        print(f)
        return
    
    lidc_uid = checkTag(xml_data.getElementsByTagName('LidcReadMessage'),"v")
    idri_uid = checkTag(xml_data.getElementsByTagName('IdriReadMessage'),"v")
    series_uid = checkTag(xml_data.getElementsByTagName('SeriesInstanceUid'))
    if series_uid == "":
        series_uid = checkTag(xml_data.getElementsByTagName('SeriesInstanceUID'))
    study_uid = xml_data.getElementsByTagName('StudyInstanceUID')[0].firstChild.nodeValue
    
    nodes = xml_data.getElementsByTagName('unblindedReadNodule')
    nodes += xml_data.getElementsByTagName('unblindedRead')
    for n in nodes:
        ID = checkTag(n.getElementsByTagName('noduleID'))
        print(ID)
        subtlety = checkTag(n.getElementsByTagName('subtlety'))
        internalStructure = checkTag(n.getElementsByTagName('internalStructure'))
        calcification = checkTag(n.getElementsByTagName('calcification'))
        sphericity = checkTag(n.getElementsByTagName('sphericity'))
        margin = checkTag(n.getElementsByTagName('margin'))
        lobulation = checkTag(n.getElementsByTagName('lobulation'))
        spiculation = checkTag(n.getElementsByTagName('spiculation'))
        texture = checkTag(n.getElementsByTagName('texture'))
        malignancy = checkTag(n.getElementsByTagName('malignancy'))
        confidence = checkTag(n.getElementsByTagName('confidence'))
        obscuration = checkTag(n.getElementsByTagName('obscuration'))
        reason = checkTag(n.getElementsByTagName('reason'))
        rois = n.getElementsByTagName('roi')
        
        for r in rois:
            z_pos = checkTag(r.getElementsByTagName('imageZposition'))
            sop_UID = r.getElementsByTagName('imageSOP_UID')[0].firstChild.nodeValue
            print(sop_UID)
            x_coord = r.getElementsByTagName('xCoord')
            y_coord = r.getElementsByTagName('yCoord')
            
            xy_coords = []
            for i in range (len(x_coord)):
                xy = (x_coord[i].firstChild.nodeValue, y_coord[i].firstChild.nodeValue)
                xy_coords.append(str(xy))
            xys = " | ".join(xy_coords)
                
            d = ["Nodule", ID, subtlety, internalStructure, calcification, sphericity, margin, lobulation, spiculation, texture, malignancy, confidence, obscuration, reason, z_pos, lidc_uid, idri_uid, series_uid, study_uid, sop_UID, xys]
            data.append(d)
        
    nodes = xml_data.getElementsByTagName('nonNodule')
    for n in nodes:
        ID = n.getElementsByTagName('nonNoduleID')[0].firstChild.nodeValue
        z_pos = n.getElementsByTagName('imageZposition')[0].firstChild.nodeValue
        x_coord = n.getElementsByTagName('xCoord')
        y_coord = n.getElementsByTagName('yCoord')
        
        xy_coords = []
        for i in range (len(x_coord)):
            xy = (x_coord[i].firstChild.nodeValue, y_coord[i].firstChild.nodeValue)
            xy_coords.append(str(xy))
        xys = " | ".join(xy_coords)
            
        sop_UID = n.getElementsByTagName('imageSOP_UID')[0].firstChild.nodeValue
        d = ["NonNodule", ID, "", "", "", "", "", "", "", "", "", "", "", "", z_pos, lidc_uid, idri_uid, series_uid, study_uid, sop_UID, xys]
        data.append(d)
    
    global filedata
    filedata[f] = data
    return data

def getUIDs():
#Collect all unique imageSOP_UIDs in LIDC-IDRI
    
    files = []
    dir_path = "/Users/vivianzhu/Documents/Annotator/Chest_and_Lung_Collections/LIDC-IDRI/LIDC-IDRI_RadiologistAnnotationsSegmentations/tcia-lidc-xml/"
    for dp,_,filenames in os.walk(dir_path):
       for f in filenames:
           if f != ".DS_Store":
               f = os.path.abspath(os.path.join(dp, f))
               files.append(f)
               print(f)

    final_data = []
    count = 0
    for f in files:
        if f not in filedata.keys():
            new_data = getData(f)
            final_data += new_data
        else:
            print("already exists")
            new_data = filedata[f]
            final_data += new_data
        count+=1
        print(count,"/",len(files) )
    
    toCSV(final_data)

getUIDs()
