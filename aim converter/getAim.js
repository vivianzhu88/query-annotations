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
    //console.log('Complete', csvData.length, 'records.'); 
    //console.log(csvData);
    //parse the array

    /*
    for (var i = 0; i < csvData.length; i++){
      var jsonObj = csvData[i];
      console.log(jsonObj);
      var aimObj = jsonToAim(jsonObj);
      console.log(aimObj);
    }
    */
    console.log('begin data parsing');
    var modData = []
    for (var i = 0; i < csvData.length; i++){

      var entry = csvData[i]
      var patient = entry['PatientID'];
      var nod = entry['Nodule/NonNodule ID'];

      node = modData.find(node => node['PatientID'] === patient && node['Nodule/NonNodule ID'] === nod);

      if (node){ // nodule + patient id combo exists
        index = modData.indexOf(node);

        modData[index]['imageSop_UID'].push(entry['imageSop_UID'])
        modData[index]['XY Coordinates'].push(entry['XY Coordinates'])
      }
      else {
        entry['imageSop_UID'] = [entry['imageSop_UID']]
        entry['XY Coordinates'] = [entry['XY Coordinates']]
        modData.push(entry)
      }

      console.log(modData.length);
    }

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

