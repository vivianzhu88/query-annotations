import pandas as pd

data_file = pd.read_csv("LIDC-IDRI.csv", dtype=str)
id_file = pd.read_csv("LIDC-IDRI_MetaData.csv", dtype=str)

terms = ["nodule"]

#filter and keep rows that contain the ID/terms we want
df = data_file[ data_file["RadLex Term"].isin(terms) | data_file["RadLex ID"].isin(terms)]

#find Patient ID and Modality
series = list(df["SeriesInstanceUID"])
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
        
df.insert(2, "PatientID", patients)
df.insert(3, "Modality", modality)
df.to_csv("new_LIDC-IDRI.csv", index=False)

