const fs = require('fs');
const papa = require('papaparse');
const file = fs.createReadStream("data_to_AIM.csv");
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

    var scan_data = {}
    for (var i = 0; i < csvData.length; i++){
      var entry = csvData[i]
      var scan_id = entry['ScanID'];

      if (scan_data[scan_id]){
        scan_data[scan_id].push(entry)
      }
      else{
        scan_data[scan_id] = [entry]
      }
    }

    for (let [key, value] of Object.entries(scan_data)){
      // create directory for each scan
      dir = "./LIDC_AIMS/Scan_" + key
      fs.mkdir(dir, { recursive: true }, (err) => {
        if (err) {
            throw err;
        }
        console.log(dir, "directory is created.");
      })

      // create an AIM file for each nodule inside the directory
      for (var j = 0; j < value.length; j++){
        console.log(j);
        var jsonObj = value[j];
        console.log(jsonObj);
        var aimObj = jsonToAim(jsonObj);
        console.log(aimObj);

        path = dir + "/" + jsonObj['Nodule/NonNodule ID'] + ".json"
        console.log(path)
        const final_data = JSON.stringify(aimObj);

        fs.writeFile(path, data, (err) => {
          if (err) {
              throw err;
          }
          console.log("JSON data is saved.");
        });

      }

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

