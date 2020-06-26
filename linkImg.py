from xml.dom import minidom
import openpyxl
from openpyxl import load_workbook
from lxml import etree
import json
import csv

filedata =  {}
#link = 'https://www.cancerimagingarchive.net/viewer/?study=' + study + '&series=' + series #useful?
def createSpreadsheet():
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.cell(row=1, column=1, value="RadLex Term")
    sheet.cell(row=1, column=2, value="RadLex ID")
    sheet.cell(row=1, column=3, value="Nodule/NonNodule")
    sheet.cell(row=1, column=4, value="Nodule/NonNodule ID")
    sheet.cell(row=1, column=5, value="Subtlety")
    sheet.cell(row=1, column=6, value="Internal Structure")
    sheet.cell(row=1, column=7, value="Calcification")
    sheet.cell(row=1, column=8, value="Sphericity")
    sheet.cell(row=1, column=9, value="Margin")
    sheet.cell(row=1, column=10, value="Lobulation")
    sheet.cell(row=1, column=11, value="Spiculation")
    sheet.cell(row=1, column=12, value="Texture")
    sheet.cell(row=1, column=13, value="Malignancy")
    sheet.cell(row=1, column=14, value="Image Z Postion")
    sheet.cell(row=1, column=15, value="LIDC ReadMessage UID")
    sheet.cell(row=1, column=16, value="IDRI ReadMessage UID")
    sheet.cell(row=1, column=17, value="SeriesInstanceUID")
    sheet.cell(row=1, column=18, value="StudyInstanceUID")
    sheet.cell(row=1, column=19, value="imageSop_UID")
    sheet.cell(row=1, column=20, value="XY Coordinates")
    workbook.save(filename="LIDC-IDRI.xlsx")
    
def toSpreadsheet(data, rterm, rid):
    workbook = load_workbook("LIDC-IDRI.xlsx")
    sheet = workbook.active
    
    for d in data:
        r = sheet.max_row+1
        sheet.cell(row=r, column=1, value=d[0])
        sheet.cell(row=r, column=2, value=d[1])
        sheet.cell(row=r, column=3, value=d[2])
        sheet.cell(row=r, column=4, value=d[3])
        sheet.cell(row=r, column=5, value=d[4])
        sheet.cell(row=r, column=6, value=d[5])
        sheet.cell(row=r, column=7, value=d[6])
        sheet.cell(row=r, column=8, value=d[7])
        sheet.cell(row=r, column=9, value=d[8])
        sheet.cell(row=r, column=10, value=d[9])
        sheet.cell(row=r, column=11, value=d[10])
        sheet.cell(row=r, column=12, value=d[11])
        sheet.cell(row=r, column=13, value=d[12])
        sheet.cell(row=r, column=14, value=d[13])
        sheet.cell(row=r, column=15, value=d[14])
        sheet.cell(row=r, column=16, value=d[15])
        sheet.cell(row=r, column=17, value=d[16])
        sheet.cell(row=r, column=18, value=d[17])
        sheet.cell(row=r, column=19, value=d[18])
        sheet.cell(row=r, column=20, value=d[19])
    
    workbook.save(filename="LIDC-IDRI.xlsx")
    
def toJson(data):
    output = []
    for d in data:
        x = {}
        x["RadLex Term"] = d[0]
        x["RadLex ID"] = d[1]
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
        x["Image Z Postion"] = d[13]
        x["LIDC ReadMessage UID"] = d[14]
        x["IDRI ReadMessage UID"] = d[15]
        x["SeriesInstanceUID"] = d[16]
        x["StudyInstanceUID"] = d[17]
        x["imageSop_UID"] = d[18]
        x["XY Coordinates"] = d[19]
        output.append(x)
        
    with open("LIDC-IDRI.json", "w") as outfile:
        json.dump(output, outfile)

def toCSV(data):
    fields = ["RadLex Term", "RadLex ID", "Nodule/NonNodule", "Nodule/NonNodule ID", "Subtlety", "Internal Structure", "Calcification", "Sphericity", "Margin", "Lobulation", "Spiculation", "Texture", "Malignancy", "Image Z Postion", "LIDC ReadMessage UID", "IDRI ReadMessage UID", "SeriesInstanceUID", "StudyInstanceUID", "imageSop_UID", "XY Coordinates"]
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
        checkTag(xml_data.getElementsByTagName('SeriesInstanceUID'))
    study_uid = xml_data.getElementsByTagName('StudyInstanceUID')[0].firstChild.nodeValue
    nodes = xml_data.getElementsByTagName('unblindedReadNodule')
    for n in nodes:
        ID = n.getElementsByTagName('noduleID')[0].firstChild.nodeValue
        subtlety = checkTag(n.getElementsByTagName('subtlety'))
        internalStructure = checkTag(n.getElementsByTagName('internalStructure'))
        calcification = checkTag(n.getElementsByTagName('calcification'))
        sphericity = checkTag(n.getElementsByTagName('sphericity'))
        margin = checkTag(n.getElementsByTagName('margin'))
        lobulation = checkTag(n.getElementsByTagName('lobulation'))
        spiculation = checkTag(n.getElementsByTagName('spiculation'))
        texture = checkTag(n.getElementsByTagName('texture'))
        malignancy = checkTag(n.getElementsByTagName('malignancy'))
        rois = n.getElementsByTagName('roi')
        
        for r in rois:
            z_pos = r.getElementsByTagName('imageZposition')[0].firstChild.nodeValue
            sop_UID = n.getElementsByTagName('imageSOP_UID')[0].firstChild.nodeValue
            x_coord = r.getElementsByTagName('xCoord')
            y_coord = r.getElementsByTagName('yCoord')
            
            xy_coords = []
            for i in range (len(x_coord)):
                xy = (x_coord[i].firstChild.nodeValue, y_coord[i].firstChild.nodeValue)
                xy_coords.append(str(xy))
            xys = " | ".join(xy_coords)
                
            d = ["Nodule", ID, subtlety, internalStructure, calcification,  sphericity, margin, lobulation, spiculation, texture, malignancy, z_pos, lidc_uid, idri_uid, series_uid, study_uid, sop_UID, xys]
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
        d = ["NonNodule", ID, "", "", "", "", "", "", "", "", "", z_pos, lidc_uid, idri_uid, series_uid, study_uid, sop_UID, xys]
        data.append(d)
    
    global filedata
    filedata[f] = data
    return data

def getUIDs():
#Collect all unique imageSOP_UIDs for each RadLex ID/term in LIDC-IDRI
    parser = etree.XMLParser(encoding='UTF-8')
    total_data = []

    with open('freq.json') as json_file:
        json_data = json.load(json_file)
        for row in json_data:
            rid = row["RIDs"]
            rterm = row["Rterms"]
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
                '''
                print("to spreadsheet")
                toSpreadsheet(data)
                print("done spreadsheet")
                '''
                total_data += r_data
            print(rterm)
    
    toJson(total_data)
    toCSV(total_data)

#Put data into Excel spreadsheet
createSpreadsheet()

getUIDs()
