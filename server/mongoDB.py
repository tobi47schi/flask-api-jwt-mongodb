from pymongo import MongoClient
import app_settings

client = MongoClient(app_settings.mongoPath)
with client:
    db = client.testdb

# db.users.drop()
db.users.create_index("email", unique=True)

