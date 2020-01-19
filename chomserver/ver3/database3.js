var sqlite3 = require('sqlite3').verbose()
var md5 = require('md5')

const DBSOURCE = "db3.sqlite" 


let db = new sqlite3.Database(DBSOURCE, (err) => {
    if (err) {
      // Cannot open database
      console.error(err.message)
      throw err
    }else{
        console.log('Connected to the SQlite database.')
        console.log('hooray');
        db.run(`CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dateTime INTEGER,
            sensorA FLOAT(4,2),
            sensorB FLOAT(4,2),
            sensorC FLOAT(4,2)
            )`,(err) => {
        if (err) {
            // Table already created
            console.log("already created");
        }else{
            // Table just created, creating some rows
            var insert = 'INSERT INTO user (dateTime,sensorA,sensorB,sensorC) VALUES (?,?,?.?)'
            var ts = Math.round((new Date()).getTime() / 1000);
            //var ts = (new Date()).getTime() / 1000;
            db.run(insert, [ts,0.0,0.0,0.0])
            //db.run(insert, [12123124,19.2,23.2])
        }
    })  
    }
})


module.exports = db

