# query-annotations
[Chest and Lung Collections data](https://drive.google.com/drive/folders/1sNpTTzbyPEroqUvzfaAT-mivW0gWe1y1?usp=sharing)

[Results](https://docs.google.com/document/d/15B_lSZQDEaRl3EwymEaHmgx4v6LPB3sqyMEEV61m2m4/edit?usp=sharing)

### Task:
Facilitate queries in TCIA chest + lung collections through imaging annotations.

### Descriptions:

1. **parseCollections.py** parses the Chest and Lung Collections data files, enters file contents into NCBO Annotator, and produces spreadsheet of filepaths and the ontology ID/terms found in it. 

2. **imgFrequencies.py** takes spreadsheet results from 1. and finds the frequency of each ontology term, ranked in decreasing order by count.

From these spreadsheets (can be found in 'Results' link above), we decided to use the CCC2018, CCC2017, and LIDC-IDRI data collections to facilitate queries.

3. **linkImg.py** is for the LIDC-IDRI collection. This parses through every file in the dataset and scrapes annotation data and DICOM image UID information.

4. **filterByRadlex.py** is for the LIDC-IDRI collection. This filters through the CSV of all LIDC-IDRI annotation data by RadLex ID or term. It also adds Patient ID and Modality info.

5. **updateTables** is for the CCC2018 and CCC2017 collections. This replaces all the Snomed CT ontology terms in the dataset with RadLex ontology terms wherever possible.

6. **aim templates** contains the templates to create AIM annotations. 

    a. **atb-** are XML format templates and it is built from the ATB platform. It is the basic structure of the template for each collection.
    
    b. **epad-** are JSON format templates created from the ATB templates. It is the template compatible with the ePAD platform.
