from core.db import get_collection
from datetime import datetime


def log_action(user, action, details):
    collection = get_collection("audit_logs")

    collection.insert_one({
        "user": user.username,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow()
    })
