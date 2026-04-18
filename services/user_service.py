import bcrypt
from core.db import get_collection


def authenticate_user(loginid, password):
    collection = get_collection("users")

    user = collection.find_one({"loginid": loginid})

    if not user:
        return None

    stored_hash = user["password"].encode("utf-8")

    if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return None

    roles = [role['name'] for role in user['roles']]
    organisations = [{'_id': org['uid'], 'name': org['name']}
                     for org in user['visitingorgs']]
    return {
        "username": f"{user["name"]} {user["thirdname"]}",
        "roles": roles,
        "organisations": organisations
    }


def authenticate_user_verification_code(loginid, verificationcode):
    collection = get_collection("users")

    user = collection.find_one({"loginid": loginid})

    if not user:
        return False

    return True if verificationcode == user['verificationcode'] else False
