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
    sheet.cell(row=1, column=5, value="Image Z Postion")
    sheet.cell(row=1, column=6, value="X Coordinate")
    sheet.cell(row=1, column=7, value="Y Coordinate")
    sheet.cell(row=1, column=8, value="imageSop_UID")
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
    
    workbook.save(filename="LIDC-IDRI.xlsx")

def getUIDs():
#Collect all unique imageSOP_UIDs for each RadLex ID/term in LIDC-IDRI
    workbook = load_workbook(filename="freq.xlsx")
    sheet = workbook.active
    parser = etree.XMLParser(encoding='UTF-8')
    
    for row in sheet.iter_rows(min_row=2, max_row=2, values_only=True):
        rid, rterm, count, filepaths = row
        files = filepaths.split(" | ")
        data = []
        for f in files:
            if f[:70] == "LIDC-IDRI/LIDC-IDRI_RadiologistAnnotationsSegmentations/tcia-lidc-xml/":
                try:
                    filepath = "Chest_and_Lung_Collections/" + f
                    xml_data = minidom.parse("Chest_and_Lung_Collections/" + f)
                    
                except (FileNotFoundError, OSError):
                    print(filepath)
                    continue
                
                nodes = xml_data.getElementsByTagName('unblindedReadNodule')
                for n in nodes:
                    ID = n.getElementsByTagName('noduleID')[0].firstChild.nodeValue
                    z_pos = n.getElementsByTagName('imageZposition')[0].firstChild.nodeValue
                    x_coord = n.getElementsByTagName('xCoord')[0].firstChild.nodeValue
                    y_coord = n.getElementsByTagName('yCoord')[0].firstChild.nodeValue
                    UID = n.getElementsByTagName('imageSOP_UID')[0].firstChild.nodeValue
                    d = [rterm, rid, "Nodule", ID, z_pos, x_coord, y_coord, UID]
                    data.append(d)
                    
                nodes = xml_data.getElementsByTagName('nonNodule')
                for n in nodes:
                    ID = n.getElementsByTagName('nonNoduleID')[0].firstChild.nodeValue
                    z_pos = n.getElementsByTagName('imageZposition')[0].firstChild.nodeValue
                    x_coord = n.getElementsByTagName('xCoord')[0].firstChild.nodeValue
                    y_coord = n.getElementsByTagName('yCoord')[0].firstChild.nodeValue
                    UID = n.getElementsByTagName('imageSOP_UID')[0].firstChild.nodeValue
                    d = [rterm, rid, "NonNodule", ID, z_pos, x_coord, y_coord, UID]
                    data.append(d)
        
        if data:
            toSpreadsheet(data)
                        

#Put data into Excel spreadsheet
#createSpreadsheet()

getUIDs()
