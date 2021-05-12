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
// get the CCC template answers for AIM
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
          code: '99EPADCCC',
          codeSystemName: '99EPAD',
          'iso:displayName': { 'xmlns:iso': 'uri:iso.org:21090', value: 'Crowds Cure Cancer' },
        }
      ];
      return { comment, modality, name, typeCode };
    }
}

function getCharacteristicsData(label, term){
// get a characteristic in the CCC template 
    our_char = term.toLowerCase()
    theData = chars.charDict[our_char]

    if(!theData){
        theData = chars.charDict["no finding"]
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
            "value": label
        },
        "uniqueIdentifier": {
            "root": generateUid()
        }
        
    }

    return data;
}


function removeEmpty(aim_json){
// remove the parents that have children with empty []
    aim_json = JSON.parse(aim_json)

    delete aim_json.ImageAnnotationCollection.imageAnnotations.ImageAnnotation[0].calculationEntityCollection
    delete aim_json.ImageAnnotationCollection.imageAnnotations.ImageAnnotation[0].imageAnnotationStatementCollection

    return aim_json
}

module.exports = function CCC2017jsonToAim(jsonObj){
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
    seedData.study.startTime = jsonObj['StudyTime'];
    seedData.study.instanceUid = jsonObj['StudyInstanceUID'];
    seedData.study.startDate = jsonObj['StudyDate'];
    seedData.study.accessionNumber = "";
    seedData.series.instanceUid = jsonObj['seriesUID'];
    seedData.series.modality = "CT";
    seedData.series.number = "";
    seedData.series.description = "";
    seedData.series.instanceNumber = "";
    seedData.equipment.manufacturerName = "";
    seedData.equipment.manufacturerModelName = "";
    seedData.equipment.softwareVersion = "";
    seedData.person.sex = "";
    seedData.person.name = "";
    seedData.person.patientId = jsonObj['patientID'];
    seedData.person.birthDate = "";

    const sopInstanceUid = jsonObj['instanceUID']
    const sopClassUid = jsonObj['SOPClassUID']

    // generate CCC template characteristics

    theChar = (getCharacteristicsData("Finding", " "))
    seedData.aim.imagingObservationEntityCollection = {
        "ImagingObservationEntity": [theChar]
    };

    thePhys = (getCharacteristicsData("Location", "jsonObj['anatomy']" ))
    seedData.aim.imagingPhysicalEntityCollection = {
        "ImagingPhysicalEntity": [thePhys]
    };    
    

    // use seed data to create AIM
    seedData.image.push({ sopClassUid, sopInstanceUid });
    const answers = getTemplateAnswers(seedData, jsonObj['order'], '');
    const merged = { ...seedData.aim, ...answers };
    seedData.aim = merged;
    seedData.user = { loginName: 'admin', name: 'admin' }
    
    console.log(JSON.stringify(seedData));
    aim = new Aim(seedData, enumAimType.imageAnnotation)

    // create markup entities
    console.log("start making markups");

    x1 = jsonObj['start_x']
    x2 = jsonObj['end_x']
    y1 = jsonObj['start_y']
    y2 = jsonObj['end_y']

    var points = []

    p1 = { x: parseFloat(x1), y: parseFloat(y1) }
    p2 = { x: parseFloat(x2), y: parseFloat(y2) }
    points.push(p1)
    points.push(p2)

    annotationType = "TwoDimensionMultiPoint"
    
    aim.addMarkupEntity(
        annotationType,
        1,
        points, // points of the roi in first image
        sopInstanceUid,
        1
    );
    
    console.log("finish making markups");
    aim_json = JSON.stringify(aim.getAimJSON())
    data = JSON.stringify(removeEmpty(aim_json))

    return data
    
}
