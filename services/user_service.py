import bcrypt
from core.db import get_collection


def authenticate_user(username, password):
    collection = get_collection("users")

    user = collection.find_one({"username": username})

    if not user:
        return None

    stored_hash = user["password"].encode("utf-8")

    if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return None

    return {
        "username": user["username"],
        "roles": user.get("roles", [])
    }
