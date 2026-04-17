LoginSessions = {
    '_id': 0,
    "LoginSessionID": {"$ifNull": ["$_id", ""]},
    "UserCode": {"$ifNull": [{"$arrayElemAt": ["$User.code", 0]}, ""]},
    "LoginDate": {
        "$dateToString": {
            "format": "%Y-%m-%d",
            "date": "$logindate",
                    "timezone": "Asia/Manila"
        }
    },
    "DefaultOrgCode": {"$ifNull": [{"$arrayElemAt": ["$DefaultOrg.code", 0]}, ""]},
    "RoleName": {"$ifNull": [{"$arrayElemAt": ["$Role.name", 0]}, ""]},
    "DepartmentCode": {"$ifNull": [{"$arrayElemAt": ["$Department.code", 0]}, ""]},
    "DepartmentName": {"$ifNull": [{"$arrayElemAt": ["$Department.name", 0]}, ""]},
}
