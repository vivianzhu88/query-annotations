const fs = require('fs');
const papa = require('papaparse');
const file = fs.createReadStream("new_LIDC-IDRI.csv");
const jsonToAim = require('./Backend.js')
const localStorage = require("localStorage")

//CSV to JSON, get entries in table
const csvData=[];
localStorage.clear();
papa.parse(file, {
  header: true,
  step: function(result) {
    csvData.push(result.data)
  },
  complete: function(results, file) {

    // organize the CSV data so each modData entry is a nodule and all of its markup info
    console.log('begin organizing data')
    var modData = []
    for (var i = 0; i < csvData.length; i++){

      var entry = csvData[i]
      var patient = entry['PatientID'];
      var nod = entry['Nodule/NonNodule ID'];

      node = modData.find(node => node['PatientID'] === patient && node['Nodule/NonNodule ID'] === nod);

      if (node){ // if nodule + patient ID combo exists, add on to the combo
        index = modData.indexOf(node);

        modData[index]['imageSop_UID'].push(entry['imageSop_UID'])
        modData[index]['XY Coordinates'].push(entry['XY Coordinates'])
      }
      else { // create the nodule + patient ID combo
        entry['imageSop_UID'] = [entry['imageSop_UID']]
        entry['XY Coordinates'] = [entry['XY Coordinates']]
        modData.push(entry)
      }

      console.log(modData.length); // finish organizing data
    }

    // create aim annotations from the data
    console.log('begin creating JSON');
    for (var j = 0; j < modData.length; j++){
      console.log(j);
      var jsonObj = modData[j];
      console.log(jsonObj);
      var aimObj = jsonToAim(jsonObj);
      console.log(aimObj);
    }
  }
});

/*function saveJson(text, filename){
    var a = document.createElement('a');
    a.setAttribute('href', 'data:text/plain;charset=utf-8,'+encodeURIComponent(text));
    a.setAttribute('download', filename);
    a.click()
}*/
//saveText(JSON.stringify(aim.getAimJSON()), "XXX.json")

