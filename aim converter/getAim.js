const fs = require('fs');
const papa = require('papaparse');
const file = fs.createReadStream("LIDC_data_to_AIM.csv");
const file2 = fs.createReadStream("CCC2017_data_to_AIM.csv");
const file3 = fs.createReadStream("CCC2018_data_to_AIM.csv");
const LIDCjsonToAim = require('./LIDC.js')
const CCC2017jsonToAim = require('./CCC2017.js')
const CCC2018jsonToAim = require('./CCC2018.js')
const localStorage = require("localStorage")

localStorage.clear();


//LIDC -------------------------------------------------------------------------------------
csvData=[];
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
        var aimObj = LIDCjsonToAim(jsonObj);
        console.log(aimObj);

        path = dir + "/" + jsonObj['Nodule/NonNodule ID'] + ".json"
        console.log(path)
        const final_data = aimObj;

        fs.writeFile(path, final_data, (err) => {
          if (err) {
              throw err;
          }
          console.log("JSON data is saved.");
        });

      }

    }

  }
});



//CCC 2017 -------------------------------------------------------------------------------------
csvData = []
papa.parse(file2, {
  header: true,
  step: function(result) {
    csvData.push(result.data)
  },
  complete: function(results, file2) {

    var collection_data = {}
    for (var i = 0; i < csvData.length; i++){
      var entry = csvData[i]
      var collection_id = entry['patientID'].slice(5,7);

      if (collection_data[collection_id]){
        collection_data[collection_id].push(entry)
      }
      else{
        collection_data[collection_id] = [entry]
      }
    }

    for (let [key, value] of Object.entries(collection_data)){
      // create directory for each scan
      dir = "./CCC2017_AIMS/TCGA_" + key
      fs.mkdir(dir, { recursive: true }, (err) => {
        if (err) {
            throw err;
        }
        console.log(dir, "directory is created.");
      })

      // create an AIM file for each annotation inside the directory
      for (var j = 0; j < value.length; j++){
        console.log(j);
        var jsonObj = value[j];
        console.log(jsonObj);
        var aimObj = CCC2017jsonToAim(jsonObj);
        console.log(aimObj);

        new_dir = dir + "/" + jsonObj['patientID'] 
        fs.mkdir(new_dir, { recursive: true }, (err) => {
          if (err) {
              throw err;
          }
          console.log(new_dir, "directory is created.");
        })

        path = new_dir + "/" + jsonObj['order'] + ".json"
        console.log(path)
        const final_data = aimObj;

        fs.writeFile(path, final_data, (err) => {
          if (err) {
              throw err;
          }
          console.log("JSON data is saved.");
        });

      }

    }

  }
});


//CCC 2018 -------------------------------------------------------------------------------------
csvData = []
papa.parse(file3, {
  header: true,
  step: function(result) {
    csvData.push(result.data)
  },
  complete: function(results, file3) {

    var collection_data = {}
    for (var i = 0; i < csvData.length; i++){
      var entry = csvData[i]
      var collection_id = entry['Collection'];

      if (collection_data[collection_id]){
        collection_data[collection_id].push(entry)
      }
      else{
        collection_data[collection_id] = [entry]
      }
    }

    for (let [key, value] of Object.entries(collection_data)){
      // create directory for each scan
      dir = "./CCC2018_AIMS/" + key
      fs.mkdir(dir, { recursive: true }, (err) => {
        if (err) {
            throw err;
        }
        console.log(dir, "directory is created.");
      })

      // create an AIM file for each annotation inside the directory
      for (var j = 0; j < value.length; j++){
        console.log(j);
        var jsonObj = value[j];
        console.log(jsonObj);
        var aimObj = CCC2018jsonToAim(jsonObj, j);
        console.log(aimObj);

        new_dir = dir + "/" + jsonObj['SubjectID'] 
        fs.mkdir(new_dir, { recursive: true }, (err) => {
          if (err) {
              throw err;
          }
          console.log(new_dir, "directory is created.");
        })

        path = new_dir + "/" + jsonObj[''] + ".json"
        console.log(path)
        const final_data = aimObj;

        fs.writeFile(path, final_data, (err) => {
          if (err) {
              throw err;
          }
          console.log("JSON data is saved.");
        });

      }
    }
  }
});
