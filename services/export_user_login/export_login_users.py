from core.db import get_collection
import pandas as pd
from services.audit_service import log_action
from .mongo_query.pipeline import get_pipeline
from tkinter import messagebox
from datetime import datetime, timedelta

# def export_to_csv(user, filters):


def export_login_users_to_csv(filters):
    try:
        collection = get_collection("loginsessions")
        start_date = filters.get("start_date")
        end_date = filters.get("end_date")
        orguid = filters.get("orguid")

        cursor = list(collection.aggregate(
            get_pipeline(start_date, end_date, orguid)))

        if not list(cursor):
            return {"status": "empty"}

        file_path = f"Login Users-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

        df = pd.DataFrame(list(cursor))

        df.to_csv(file_path, index=False)
        messagebox.showinfo("Export Successful",
                            f"Data exported to {file_path}")

        return {
            "status": "success",
            "file": file_path,
            "data": df
        }

    except Exception as e:
        raise e
