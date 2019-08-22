from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
with client:
    db = client.testdb

# db.users.drop()
db.users.create_index("email", unique=True)
