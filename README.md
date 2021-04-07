# Description:
In my project, I first worked with the National Center for Biomedical Ontology’s Annotator and utilized its capabilities to annotate for radiology terms and references in studies. I incorporated this tool in a program I wrote, which parses through 21 chest and lung CT collections from The Cancer Imaging Archive. These collections contain information about thousands of patient studies, and my program searches for notes written by radiologists and feeds the text data to the Annotator. 

After fetching all the annotations, I did a frequency analysis on the results and looked for terms that could be queried, such as “malignancy,” “lobulation,” and “nodule.” Finding these terms, I was able to locate which collections contained them, and I narrowed down to three collections that I would focus on creating queries for.

Within these three collections, I parsed all the files to look for useful data related to these annotations, such as descriptions of the size, shape, and type of nodules. I mapped the annotations and the descriptions to the DICOM unique identifiers of their according files. In this step, I had to generate AIM files that would be viewable on Stanford’s ePAD, which is a quantitative imaging informatics platform. The CT scan and additional annotation information also had to be displayed.

Lastly, I queried these AIM files, which allows a user to search for a term, such as “nodule,” causing all matching AIM files and their relevant information to appear. 

# Data
[Chest and Lung Collections data](https://drive.google.com/drive/folders/1sNpTTzbyPEroqUvzfaAT-mivW0gWe1y1?usp=sharing)

[Results](https://docs.google.com/document/d/15B_lSZQDEaRl3EwymEaHmgx4v6LPB3sqyMEEV61m2m4/edit?usp=sharing)

### Task:
Facilitate queries in TCIA chest + lung collections through imaging annotations.

### Files:

1. **parseCollections.py** parses the Chest and Lung Collections data files, enters file contents into NCBO Annotator, and produces spreadsheet of filepaths and the ontology ID/terms found in it. 

2. **imgFrequencies.py** takes spreadsheet results from 1. and finds the frequency of each ontology term, ranked in decreasing order by count.

From these spreadsheets (can be found in 'Results' link above), we decided to use the CCC2018, CCC2017, and LIDC-IDRI data collections to facilitate queries.

3. **linkImg.py** is for the LIDC-IDRI collection. This parses through every file in the dataset and scrapes annotation data and DICOM image UID information.

4. **addExtraValues.py** is for the LIDC-IDRI collection. It adds Patient ID and Modality info to the LIDC data.

5. **queryLIDC.py** is for the LIDC-IDRI collection. It queries LIDC data and prepares it for the AIM conversion code.

6. **updateTables** is for the CCC2018 and CCC2017 collections. This replaces all the Snomed CT ontology terms in the dataset with RadLex ontology terms wherever possible.

7. **aim templates** contains the templates to create AIM annotations. 

    a. **atb-** are XML format templates and it is built from the ATB platform. It is the basic structure of the template for each collection. [xml to json](https://github.com/RubinLab/aimconvert)
    
    b. **epad-** are JSON format templates created from the ATB templates. It is the template compatible with the ePAD platform.
