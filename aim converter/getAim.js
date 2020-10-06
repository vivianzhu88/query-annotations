const fs = require('fs');
const papa = require('papaparse');
const file = fs.createReadStream("new_LIDC-IDRI.csv");
const backend = require('Backend')

//CSV to JSON, get entries in table
var csvData=[];
papa.parse(file, {
  header: true,
  step: function(result) {
    csvData.push(result.data)
  },
  complete: function(results, file) {
    //console.log('Complete', csvData.length, 'records.'); 
    console.log(csvData);
  }
});

//parse the array
for (var i = 0; i < csvData.length; i++){
    var jsonObj = csvData[i];
    let aimObj = backend.jsonToAim(jsonObj);
}

/*function saveJson(text, filename){
    var a = document.createElement('a');
    a.setAttribute('href', 'data:text/plain;charset=utf-8,'+encodeURIComponent(text));
    a.setAttribute('download', filename);
    a.click()
}*/
//saveText(JSON.stringify(aim.getAimJSON()), "XXX.json")

