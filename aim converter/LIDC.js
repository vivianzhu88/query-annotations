const { Aim } = require("aimapi");
const chars = require("./characteristics.js")
const localStorage = require("localStorage")

const enumAimType = {
  imageAnnotation: 1,
  seriesAnnotation: 2,
  studyAnnotation: 3,
};

function generateUid() {
//generate random UIDs
    let uid = "2.25." + Math.floor(1 + Math.random() * 9);
    for (let index = 0; index < 38; index++) {
      uid = uid + Math.floor(Math.random() * 10);
    }
    return uid;
  }

function getTemplateAnswers(metadata, annotationName, tempModality) {
// get the LIDC template answers for AIM
    if (metadata.series) {
      const { number, description, instanceNumber } = metadata.series;
      const seriesModality = metadata.series.modality;
      const comment = {
        value: `${seriesModality} / ${description} / ${instanceNumber} / ${number}`,
      };
      const modality = { value: tempModality };
      const name = { value: annotationName };
      const typeCode = [
        {
          code: 'LIDC-IDRI',
          codeSystemName: 'LIDC-IDRI',
          'iso:displayName': { 'xmlns:iso': 'uri:iso.org:21090', value: 'LIDC-IDRI' },
        }
      ];
      return { comment, modality, name, typeCode };
    }
}

function getCharacteristicsData(label, labelValue){
// get a characteristic in the LIDC template 
    our_char = label.toLowerCase() + labelValue
    theData = chars.charDict[our_char]

    if(!theData) {
        theData = {
            "code": "out of range",
            "codeSystemName": "LIDC-IDRI",
            "codeSystemVersion": "",
            "displayValue": "out of range",
            "displayXmlns": "uri:iso.org:21090",
            "labelValue": label.toLowerCase()
        }
    }  

    data = {
        "typeCode": [
            {
                "code": theData.code,
                "codeSystemName": theData.codeSystemName,
                "codeSystemVersion": theData.codeSystemVersion,
                "iso:displayName": {
                    "value": theData.displayValue,
                    "xmlns:iso": theData.displayXmlns
                }
            }
        ],
        "annotatorConfidence": {
            "value": 0
        },
        "label": {
            "value": label.toLowerCase()
        }
    }

    return data;
}


function removeEmpty(aim_json){
// remove the parents that have children with empty []
    aim_json = JSON.parse(aim_json)

    delete aim_json.ImageAnnotationCollection.imageAnnotations.ImageAnnotation[0].calculationEntityCollection
    delete aim_json.ImageAnnotationCollection.imageAnnotations.ImageAnnotation[0].imageAnnotationStatementCollection

    if (aim_json.ImageAnnotationCollection.imageAnnotations.ImageAnnotation[0].imagingObservationEntityCollection.ImagingObservationEntity[0].imagingObservationCharacteristicCollection.ImagingObservationCharacteristic.length == 0){
        delete aim_json.ImageAnnotationCollection.imageAnnotations.ImageAnnotation[0].imagingObservationEntityCollection.ImagingObservationEntity[0].imagingObservationCharacteristicCollection
    }
    return aim_json
}

module.exports = function jsonToAim(jsonObj){
    console.log("json")
    const seedData = {};
    seedData.aim = {};
    seedData.study = {};
    seedData.series = {};
    seedData.equipment = {};
    seedData.person = {};
    seedData.image = [];

    // generate seed data basics
    seedData.aim.studyInstanceUid = jsonObj['StudyInstanceUID'];
    seedData.study.startTime = "";
    seedData.study.instanceUid = jsonObj['StudyInstanceUID'];
    seedData.study.startDate = "";
    seedData.study.accessionNumber = "";
    seedData.series.instanceUid = jsonObj['SeriesInstanceUID'];
    seedData.series.modality = jsonObj['Modality'];
    seedData.series.number = "";
    seedData.series.description = "";
    seedData.series.instanceNumber = "";
    seedData.equipment.manufacturerName = "";
    seedData.equipment.manufacturerModelName = "";
    seedData.equipment.softwareVersion = "";
    seedData.person.sex = "";
    seedData.person.name = "";
    seedData.person.patientId = jsonObj['PatientID'];
    seedData.person.birthDate = "";
    
    if (jsonObj['Modality'] == 'DX'){
        sopClassUid = "1.2.840.10008.5.1.4.1.1.1.1";
    }
    else if (jsonObj['Modality'] == 'CR'){
        sopClassUid = "1.2.840.10008.5.1.4.1.1.1";
    }
    else { // (jsonObj['Modality'] == 'CT')
        sopClassUid = "1.2.840.10008.5.1.4.1.1.2";
    }

    var uids = jsonObj['imageSop_UID'].split('*')
    const sopInstanceUid = uids[0];

    // generate LIDC template characteristics
    if (jsonObj['Nodule/NonNodule'] == 'Nodule'){

        var theChars = []
        if (jsonObj['Subtlety'] != ''){

            theChars.push(getCharacteristicsData('Subtlety', jsonObj['Subtlety']))
        }
        if (jsonObj['Internal Structure'] != ''){
            theChars.push(getCharacteristicsData('Internal Structure', jsonObj['Internal Structure']))
        }
        if (jsonObj['Calcification'] != ''){
            theChars.push(getCharacteristicsData('Calcification', jsonObj['Calcification']))
        }
        if (jsonObj['Sphericity'] != ''){
            theChars.push(getCharacteristicsData('Sphericity', jsonObj['Sphericity']))
        }
        if (jsonObj['Margin'] != ''){
            theChars.push(getCharacteristicsData('Margin', jsonObj['Margin']))
        }
        if (jsonObj['Lobulation'] != ''){
            theChars.push(getCharacteristicsData('Lobulation', jsonObj['Lobulation']))
        }
        if (jsonObj['Spiculation'] != ''){
            theChars.push(getCharacteristicsData('Spiculation', jsonObj['Spiculation']))
        }
        if (jsonObj['Texture'] != ''){
            theChars.push(getCharacteristicsData('Texture', jsonObj['Texture']))
        }
        if (jsonObj['Malignancy'] != ''){
            theChars.push(getCharacteristicsData('Malignancy', jsonObj['Malignancy']))
        }

        seedData.aim.imagingObservationEntityCollection = {
            "ImagingObservationEntity": [
                {
                    "typeCode": [
                        {
                            "code": "nodule",
                            "codeSystemName": "LIDC-IDRI",
                            "iso:displayName": {
                                "value": "nodule",
                                "xmlns:iso": "uri:iso.org:21090"
                            }
                        }
                    ],
                    "annotatorConfidence": {
                        "value": 0
                    },
                    "label": {
                        "value": "Nodule"
                    },
                    "uniqueIdentifier": {
                        "root": generateUid()
                    },
                    "imagingObservationCharacteristicCollection": {
                        "ImagingObservationCharacteristic": theChars
                    }
                }
            ]
        };
    }

    // use seed data to create AIM
    seedData.image.push({ sopClassUid, sopInstanceUid });
    const answers = getTemplateAnswers(seedData, jsonObj['Nodule/NonNodule ID'], '');
    const merged = { ...seedData.aim, ...answers };
    seedData.aim = merged;
    seedData.user = { loginName: 'admin', name: 'admin' }
    
    console.log(JSON.stringify(seedData));
    aim = new Aim(seedData, enumAimType.imageAnnotation)
    
    var uids = jsonObj['imageSop_UID'].split('*')
    var coords = jsonObj['XY Coordinates'].split('*')

    // create markup entities
    console.log("start making markups");
    for (var i = 0; i < uids.length; i++){

        // fix formatting 
        points = coords[i].split('|')
        // create the markup points
        modPoints = []
        for (var j = 0; j < points.length; j++){
            p = points[j]
            p = p.replace(/'/g,"")
            p = p.replace(/\s+/,"")
            p = p.slice(1, -1)
            p = p.split(',')
            point = { x: parseFloat(p[0]), y: parseFloat(p[1]) }
            modPoints.push(point)
        }
        count = i+1
        if (modPoints.length == 1){
            annotationType = "TwoDimensionPoint"
        }
        else{
            annotationType = "TwoDimensionPolyline"
        }
        
        aim.addMarkupEntity(
            annotationType,
            1,
            modPoints, // points of the roi in first image
            uids[i], // first image
            count
        );
    }
    console.log("finish making markups");
    aim_json = JSON.stringify(aim.getAimJSON())
    data = JSON.stringify(removeEmpty(aim_json))

    return data
    
}
