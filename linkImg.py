from xml.dom import minidom
import openpyxl
from openpyxl import load_workbook
from lxml import etree

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
    sheet.cell(row=1, column=15, value="imageSop_UID")
    sheet.cell(row=1, column=16, value="XY Coordinates")
    workbook.save(filename="LIDC-IDRI.xlsx")
    
def toSpreadsheet(data):
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
    
    workbook.save(filename="LIDC-IDRI.xlsx")

def checkTag(tag):
    if tag:
        return tag[0].firstChild.nodeValue
    else:
        return ""

def getUIDs():
#Collect all unique imageSOP_UIDs for each RadLex ID/term in LIDC-IDRI
    workbook = load_workbook(filename="freq.xlsx")
    sheet = workbook.active
    parser = etree.XMLParser(encoding='UTF-8')
    
    filedata  = {}
    for row in sheet.iter_rows(min_row=2, values_only=True):
        rid, rterm, count, filepaths = row
        files = filepaths.split(" | ")
        data = []
        print(count)
        print(len(files))
        count =  0
        for f in files:
            if f[:70] == "LIDC-IDRI/LIDC-IDRI_RadiologistAnnotationsSegmentations/tcia-lidc-xml/":
                if f not in filedata.keys():
                    try:
                        filepath = "Chest_and_Lung_Collections/" + f
                        xml_data = minidom.parse("Chest_and_Lung_Collections/" + f)
                        
                    except (FileNotFoundError, OSError):
                        print(filepath)
                        continue
                    
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
                            UID = n.getElementsByTagName('imageSOP_UID')[0].firstChild.nodeValue
                            x_coord = r.getElementsByTagName('xCoord')
                            y_coord = r.getElementsByTagName('yCoord')
                            
                            xy_coords = []
                            for i in range (len(x_coord)):
                                xy = (x_coord[i].firstChild.nodeValue, y_coord[i].firstChild.nodeValue)
                                xy_coords.append(str(xy))
                            xys = " | ".join(xy_coords)
                                
                            d = [rterm, rid, "Nodule", ID, subtlety, internalStructure, calcification,  sphericity, margin, lobulation, spiculation, texture, malignancy, z_pos, UID, xys]
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
                            
                        UID = n.getElementsByTagName('imageSOP_UID')[0].firstChild.nodeValue
                        d = [rterm, rid, "NonNodule", ID, "", "", "", "", "", "", "", "", "", z_pos, UID, xys]
                        data.append(d)
                    filedata[f] = data
                else:
                    print("already exists")
                    data = filedata[f]
                count+=1
                print(count,"/",len(files) )
        
        if data:
            print(toSpreadsheet)
            toSpreadsheet(data)
        print(rterm)
                        

#Put data into Excel spreadsheet
#createSpreadsheet()

getUIDs()
