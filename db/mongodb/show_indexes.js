indexes = db[collection].getIndexes();
print("Indexes for " + collection + ":");
printjson(indexes);