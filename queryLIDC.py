import pylidc as pl
import pandas as pd

#Fetch all LIDC-IDRI scans
#** - means value goes into AIM

def query():
#Collect queried LIDC data
    '''
    insert future query stuff
    '''
    
    scans = pl.query(pl.Scan)
    print("We have", scans.count(), "LIDC-IDRI scans")

    #Use LIDC database from values scraped from .xml because the pylidc library doesn't have anything to access the "imageSop_UID" values
    lidc_database = pd.read_csv("new_LIDC-IDRI.csv", dtype=str)
    
    print(lidc_database["Modality"].unique())

    aims = []
    for scan in scans:
        study_uid = scan.study_instance_uid #**
        series_uid = scan.series_instance_uid #**
        patient = scan.patient_id #**
        scan_id = scan.id #**
        
        #Get all 'nodule' data entries for the scan instance
        scan_database = lidc_database[(lidc_database["SeriesInstanceUID"] == series_uid) & (lidc_database["StudyInstanceUID"] == study_uid) & (lidc_database["Nodule/NonNodule"] == "Nodule") & (lidc_database["PatientID"] == patient)]
        
        #Organize into nodule groups
        nodules = scan_database["Nodule/NonNodule ID"].unique()
        print(nodules)
        
        for n in nodules:
            nod_database = scan_database[(scan_database["Nodule/NonNodule ID"] == n)]
            
            #Fetch data for AIM file entry
            mod = nod_database["Modality"].values[0] #**
            nod = nod_database["Nodule/NonNodule"].values[0] #**
            nod_id = nod_database["Nodule/NonNodule ID"].values[0] #**
            sub = nod_database["Subtlety"].values[0] #**
            i_s = nod_database["Internal Structure"].values[0] #**
            cal = nod_database["Calcification"].values[0] #**
            sph = nod_database["Sphericity"].values[0] #**
            mar = nod_database["Margin"].values[0] #**
            lob = nod_database["Lobulation"].values[0] #**
            spi = nod_database["Spiculation"].values[0] #**
            tex = nod_database["Texture"].values[0] #**
            mal = nod_database["Malignancy"].values[0] #**
        
            image_sop_uids = "*".join(nod_database["imageSop_UID"].tolist()) #**
            XYcoords = "*".join(nod_database["XY Coordinates"].tolist()) #**
            
            aim = [scan_id, patient, mod, nod, nod_id, sub, i_s, cal, sph, mar, lob, spi, tex, mal, series_uid, study_uid, image_sop_uids, XYcoords]
            
            #Add AIM file entry into AIM database
            aims.append(aim)
            
    aim_df = pd.DataFrame(aims, columns = ["ScanID", "PatientID", "Modality", "Nodule/NonNodule", "Nodule/NonNodule ID", "Subtlety", "Internal Structure", "Calcification", "Sphericity", "Margin", "Lobulation", "Spiculation", "Texture", "Malignancy", "SeriesInstanceUID", "StudyInstanceUID", "imageSop_UID", "XY Coordinates"])
    aim_df.to_csv("data_to_AIM.csv", index=False)
        
query()
