import bcrypt
from core.db import get_collection


def authenticate_user(loginid, password):
    collection = get_collection("users")

    user = collection.find_one({"loginid": loginid})

    if not user:
        return None

    stored_hash = user["password"].encode("utf-8")
    roles = [role['name'] for role in user['roles']]
    if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return None

    return {
        "username": f"{user["name"]} {user["thirdname"]}",
        "roles": roles
    }
# ThinkPad@L14
