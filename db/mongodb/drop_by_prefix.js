db = db.getSiblingDB('admin');
dbs = db.runCommand({ "listDatabases": 1 }).databases;
dbs.forEach(function(database) {
    if(database.name.indexOf(prefix) !== -1) {
        db.getSiblingDB(database.name).dropDatabase();
    }
});
