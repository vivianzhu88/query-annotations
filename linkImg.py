from xml.dom import minidom
import openpyxl
from openpyxl import load_workbook
from lxml import etree
import json
import csv

filedata =  {}
    
def toJson(data):
#LIDC-IDRI data to json format
    output = []
    for d in data:
        x = {}
        x["NCIT Term"] = d[0]
        x["NCIT ID"] = d[1]
        x["Nodule/NonNodule"] = d[2]
        x["Nodule/NonNodule ID"] = d[3]
        x["Subtlety"] = d[4]
        x["Internal Structure"] = d[5]
        x["Calcification"] = d[6]
        x["Sphericity"] = d[7]
        x["Margin"] = d[8]
        x["Lobulation"] = d[9]
        x["Spiculation"] = d[10]
        x["Texture"] = d[11]
        x["Malignancy"] = d[12]
        x["Confidence"] = d[13]
        x["Obscuration"] = d[14]
        x["Reason"] = d[15]
        x["Image Z Postion"] = d[16]
        x["LIDC ReadMessage UID"] = d[17]
        x["IDRI ReadMessage UID"] = d[18]
        x["SeriesInstanceUID"] = d[19]
        x["StudyInstanceUID"] = d[20]
        x["imageSop_UID"] = d[21]
        x["XY Coordinates"] = d[22]
        output.append(x)
        
    with open("LIDC-IDRI.json", "w") as outfile:
        json.dump(output, outfile)

def toCSV(data):
#LIDC-IDRI data to csv format
    fields = ["NCIT Term", "NCIT ID", "Nodule/NonNodule", "Nodule/NonNodule ID", "Subtlety", "Internal Structure", "Calcification", "Sphericity", "Margin", "Lobulation", "Spiculation", "Texture", "Malignancy", "Confidence", "Obscuration", "Reason", "Image Z Postion", "LIDC ReadMessage UID", "IDRI ReadMessage UID", "SeriesInstanceUID", "StudyInstanceUID", "imageSop_UID", "XY Coordinates"]
    rows = data
    filename = "LIDC-IDRI.csv"
    
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

def checkTag(tag, v=None):
#check tag for values
    if tag:
        if v is None:
            return tag[0].firstChild.nodeValue
        else:
            return tag[0].attributes.get("uid").value
    else:
        return ""


def getData(f):
#parse LIDC-IDRI radiologist annotation files
    data = []
    try:
        filepath = "Chest_and_Lung_Collections/" + f
        xml_data = minidom.parse("Chest_and_Lung_Collections/" + f)
        print(f)
        
    except (FileNotFoundError, OSError):
        print(filepath)
        return
    
    lidc_uid = checkTag(xml_data.getElementsByTagName('LidcReadMessage'),"v")
    idri_uid = checkTag(xml_data.getElementsByTagName('IdriReadMessage'),"v")
    series_uid = checkTag(xml_data.getElementsByTagName('SeriesInstanceUid'))
    if series_uid == "":
        series_uid = checkTag(xml_data.getElementsByTagName('SeriesInstanceUID'))
    study_uid = xml_data.getElementsByTagName('StudyInstanceUID')[0].firstChild.nodeValue
    
    #parse for Nodules
    nodes = xml_data.getElementsByTagName('unblindedReadNodule')
    nodes += xml_data.getElementsByTagName('unblindedRead')
    for n in nodes:
        ID = checkTag(n.getElementsByTagName('noduleID'))
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
            sop_UID = n.getElementsByTagName('imageSOP_UID')[0].firstChild.nodeValue
            x_coord = r.getElementsByTagName('xCoord')
            y_coord = r.getElementsByTagName('yCoord')
            
            xy_coords = []
            for i in range (len(x_coord)):
                xy = (x_coord[i].firstChild.nodeValue, y_coord[i].firstChild.nodeValue)
                xy_coords.append(str(xy))
            xys = " | ".join(xy_coords)
                
            d = ["Nodule", ID, subtlety, internalStructure, calcification, sphericity, margin, lobulation, spiculation, texture, malignancy, confidence, obscuration, reason, z_pos, lidc_uid, idri_uid, series_uid, study_uid, sop_UID, xys]
            data.append(d)
        
    #parse for NonNodules
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
#summarize LIDC-IDRI files
    parser = etree.XMLParser(encoding='UTF-8')
    total_data = []

    with open('freq.json') as json_file:
        json_data = json.load(json_file)
        for row in json_data:
            rid = row["NIDs"]
            rterm = row["Nterms"]
            count = row["Count"]
            filepaths = row["File Paths"]
            files = filepaths.split(" | ")
            
            r_data = []
            count =  0
            for f in files:
                if f[:70] == "LIDC-IDRI/LIDC-IDRI_RadiologistAnnotationsSegmentations/tcia-lidc-xml/":
                    if f not in filedata.keys():
                        new_data = [ ([rterm, rid] + x) for x in getData(f)]
                        r_data += new_data
                    else:
                        print("already exists")
                        new_data = [ ([rterm, rid] + x) for x in filedata[f]]
                        r_data += new_data
                    count+=1
                    print(count,"/",len(files) )
            
            if r_data:
                total_data += r_data
            print(rterm)
    
    toJson(total_data)
    toCSV(total_data)


getUIDs()
