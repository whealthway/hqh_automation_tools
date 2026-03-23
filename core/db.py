from pymongo import MongoClient
from config.settings import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def get_collection(name):
    return db[name]


def get_organisations():
    return list(db["organisations"].find({}, {"_id": 1, "name": 1, "code": 1}))


def get_visit_orders():
    return list(db["patientorders"].aggregate([{}], {"_id": 1, "visitid": 1, "orguid": 1}))
