import pymongo

connection = pymongo.MongoClient("mongodb://db:27017") # MongoDB Connection
db = connection['vehicle_info']
db.drop_collection('admin_docs')
db.drop_collection('user_docs')
db.drop_collection('vehicle_docs')
