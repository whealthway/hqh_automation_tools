from core.db import get_collection
import pandas as pd
from services.audit_service import log_action
from .mongo_query.pipeline import get_pipeline
from tkinter import messagebox
from datetime import datetime
from passlib.hash import bcrypt

# def export_to_csv(user, filters):


def validate_user(filters):
    try:
        collection = get_collection("users")
        loginid = filters.get("loginid")
        password = filters.get("password")
        cursor = list(collection.aggregate(get_pipeline(loginid)))

        if cursor:
            user = cursor[0]  # assuming 1 user per loginid
            stored_hash = user.get("password")  # adjust field name if needed

            if stored_hash and bcrypt.verify(password, stored_hash):
                return True
                # proceed with user data
            else:
                return False

    except Exception as e:
        raise e
