const { Aim } = require("aimapi");

const enumAimType = {
  imageAnnotation: 1,
  seriesAnnotation: 2,
  studyAnnotation: 3,
};

function generateUid() {
    let uid = "2.25." + Math.floor(1 + Math.random() * 9);
    for (let index = 0; index < 38; index++) {
      uid = uid + Math.floor(Math.random() * 10);
    }
    return uid;
  }
console.log(generateUid());

function getTemplateAnswers(metadata, annotationName, tempModality) {
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
          code: 'ROI',
          codeSystemName: '99EPAD',
          'iso:displayName': { 'xmlns:iso': 'uri:iso.org:21090', value: 'ROI Only' },
        },
      ];
      return { comment, modality, name, typeCode };
    }
  }

export function jsonToAim(jsonObj){
    this.seedData = {};
    this.seedData.aim = {};
    this.seedData.study = {};
    this.seedData.series = {};
    this.seedData.equipment = {};
    this.seedData.person = {};
    this.seedData.image = [];

    this.seedData.aim.studyInstanceUid = jsonObj['StudyInstanceUID'];
    this.seedData.study.startTime = "";
    this.seedData.study.instanceUid = jsonObj['StudyInstanceUID'];
    this.seedData.study.startDate = "";
    this.seedData.study.accessionNumber = "";
    this.seedData.series.instanceUid = jsonObj['SeriesInstanceUID'];
    this.seedData.series.modality = jsonObj['Modality'];
    this.seedData.series.number = "";
    this.seedData.series.description = "";
    this.seedData.series.instanceNumber = "";
    this.seedData.equipment.manufacturerName = "";
    this.seedData.equipment.manufacturerModelName = "";
    this.seedData.equipment.softwareVersion = "";
    this.seedData.person.sex = "";
    this.seedData.person.name = "";
    this.seedData.person.patientId = jsonObj['Patient ID'];
    this.seedData.person.birthDate = "";
    this.sopClassUid = jsonObj['SOPClassUID'];
    this.sopInstanceUid = jsonObj['SOPInstanceUID'];
}

// fill in the seed data

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
                "root": "2.25.870780621633412196796041908505416068723"
            },
            "imagingObservationCharacteristicCollection": {
                "ImagingObservationCharacteristic": [
                    {
                        "typeCode": [
                            {
                                "code": "very subtle",
                                "codeSystemName": "LIDC-IDRI",
                                "iso:displayName": {
                                    "value": "very subtle",
                                    "xmlns:iso": "uri:iso.org:21090"
                                }
                            }
                        ],
                        "annotatorConfidence": {
                            "value": 0
                        },
                        "label": {
                            "value": "subtlety"
                        }
                    },
                    {
                        "typeCode": [
                            {
                                "code": "C12471",
                                "codeSystemName": "NCIT",
                                "codeSystemVersion": "1.0",
                                "iso:displayName": {
                                    "value": "soft tissue",
                                    "xmlns:iso": "uri:iso.org:21090"
                                }
                            }
                        ],
                        "annotatorConfidence": {
                            "value": 0
                        },
                        "label": {
                            "value": "internal structure"
                        }
                    },
                    {
                        "typeCode": [
                            {
                                "code": "popcorn",
                                "codeSystemName": "LIDC-IDRI",
                                "iso:displayName": {
                                    "value": "popcorn",
                                    "xmlns:iso": "uri:iso.org:21090"
                                }
                            }
                        ],
                        "annotatorConfidence": {
                            "value": 0
                        },
                        "label": {
                            "value": "calcification"
                        }
                    },
                    {
                        "typeCode": [
                            {
                                "code": "RID5800",
                                "codeSystemName": "RadLex",
                                "codeSystemVersion": "1.0",
                                "iso:displayName": {
                                    "value": "oval",
                                    "xmlns:iso": "uri:iso.org:21090"
                                }
                            }
                        ],
                        "annotatorConfidence": {
                            "value": 0
                        },
                        "label": {
                            "value": "sphericity"
                        }
                    },
                    {
                        "typeCode": [
                            {
                                "code": "fairly defined",
                                "codeSystemName": "LIDC-IDRI",
                                "iso:displayName": {
                                    "value": "fairly defined",
                                    "xmlns:iso": "uri:iso.org:21090"
                                }
                            }
                        ],
                        "annotatorConfidence": {
                            "value": 0
                        },
                        "label": {
                            "value": "margin"
                        }
                    },
                    
                ]
            }
        }
    ]
};
seedData.image.push({ sopClassUid, sopInstanceUid });


const answers = getTemplateAnswers(seedData, 'nodule1', '');
const merged = { ...seedData.aim, ...answers };
seedData.aim = merged;
seedData.user = { loginName: 'admin', name: 'admin' }

const aim = new Aim(seedData, enumAimType.imageAnnotation);

// add the markups
// points is an array of items { x: parseFloat(x), y: parseFloat(y) }
// aim.addMarkupEntity(
//   "TwoDimensionPolyline",
//   1,
//   points, // points of the roi in first image
//   imageReferenceUid, // first image
//   1
// );
// aim.addMarkupEntity(
//     "TwoDimensionPolyline",
//     2,
//     points, // points of the roi in 2nd image
//     imageReferenceUid, // 2nd image imge sop instance uid
//     1
//   );
// add characteristics

console.log(JSON.stringify(aim.getAimJSON())); // to get the aim json seedDataect

