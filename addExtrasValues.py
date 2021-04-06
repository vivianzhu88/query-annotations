import pandas as pd

data_file = pd.read_csv("LIDC-IDRI.csv", dtype=str)
id_file = pd.read_csv("LIDC-IDRI_MetaData.csv", dtype=str)

#find Patient ID and Modality
series = list(data_file["SeriesInstanceUID"])
patients = []
modality = []

p = list(id_file["Patient Id"])
m = list(id_file["Modality"])
p_series = list(id_file["Series UID"])

for i in range (len(series)):
    if series[i] in p_series:
        j = p_series.index(series[i])
        patients.append(p[j])
        modality.append(m[j])
    else:
        patients.append("")
        modality.append("")
        
data_file.insert(0, "PatientID", patients)
data_file.insert(1, "Modality", modality)
data_file.to_csv("new_LIDC-IDRI.csv", index=False)


