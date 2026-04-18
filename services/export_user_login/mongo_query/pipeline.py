from .projection import LoginSessions
from bson import ObjectId


def get_pipeline(start_date, end_date, orguid):
    return [
        {
            '$match': {
                "orguid": ObjectId(orguid),
                'logindate': {
                    '$gte': start_date,
                    '$lt': end_date
                },
                'useruid': {'$exists': True}
            }
        },
        {
            '$lookup': {
                'from': 'organisations',
                'localField': 'orguid',
                'foreignField': '_id',
                'as': 'Org'
            }
        },
        {
            '$lookup': {
                'from': 'departments',
                'localField': 'departmentuid',
                'foreignField': '_id',
                'as': 'Department'
            }
        },
        {
            '$lookup': {
                'from': 'roles',
                'localField': 'roleuid',
                'foreignField': '_id',
                'as': 'Role'
            }
        },
        {
            '$lookup': {
                'from': 'users',
                'localField': 'useruid',
                'foreignField': '_id',
                'as': 'User',
            }
        },
        {
            '$lookup': {
                'from': 'organisations',
                'localField': 'User.defaultorguid',
                'foreignField': '_id',
                'as': 'DefaultOrg'
            }
        },
        {
            '$project': LoginSessions
        }
    ]
