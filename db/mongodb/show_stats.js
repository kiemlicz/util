db = db.getSiblingDB('admin');
dbs = db.runCommand({ "listDatabases": 1 }).databases;
dbs.forEach(function(database) {
    //in kb
    printjson(db.getSiblingDB(database.name).stats(1024));
});
