from openpyxl import load_workbook
from xml.dom import minidom
import openpyxl

#link = 'https://www.cancerimagingarchive.net/viewer/?study=' + study + '&series=' + series #useful?

def getUIDs():
#Collect all unique imageSOP_UIDs for each RadLex ID/term in LIDC-IDRI
    workbook = load_workbook(filename="freq.xlsx")
    sheet = workbook.active
    UIDs = []
    for row in sheet.iter_rows(min_row=3, values_only=True):
        rid, rterm, count, filepaths = row
        files = filepaths.split(" | ")
        for f in files:
            if f[:9] == "LIDC-IDRI":
                xml_data = minidom.parse("Chest_and_Lung_Collections/" + f)
                all_imageSOP_UIDs = xml_data.getElementsByTagName('imageSOP_UID')
                for item in all_imageSOP_UIDs:
                    if [rterm, rid, item.firstChild.nodeValue] not in UIDs:
                        UIDs.append([rterm, rid, item.firstChild.nodeValue])
    UIDs.sort(key=lambda x: x[0])
    return UIDs

#Put data into Excel spreadsheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.cell(row=1, column=1, value="RadLex Term")
sheet.cell(row=1, column=2, value="RadLex ID")
sheet.cell(row=1, column=3, value="UID")

data = getUIDs()
row = 2
for d in data:
    if len(d) == 3:
        sheet.cell(row=row, column=1, value=d[0])
        sheet.cell(row=row, column=2, value=d[1])
        sheet.cell(row=row, column=3, value=d[2])
        row += 1

workbook.save(filename="LIDC-IDRI.xlsx")
                


        
        
