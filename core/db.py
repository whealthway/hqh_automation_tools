from pymongo import MongoClient
from config.settings import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def get_collection(name):
    return db[name]


def get_organisations(loginid):
    return list(db["users"].aggregate([
        {'$match': {'loginid': loginid}},
        {'$unwind': '$visitingorgs'},
        {
            '$project': {
                '_id': '$uid',
                'name': 1
            }
        }
    ]))


def get_visit_orders():
    return list(db["patientorders"].aggregate([{}], {"_id": 1, "visitid": 1, "orguid": 1}))
