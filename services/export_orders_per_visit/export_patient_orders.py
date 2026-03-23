from core.db import get_collection
import pandas as pd
from services.audit_service import log_action
from .mongo_query.pipeline import get_pipeline
from tkinter import messagebox
from datetime import datetime

# def export_to_csv(user, filters):


def export_to_csv(filters):
    try:
        collection = get_collection("patientorders")
        visitid = filters.get("visitid")
        orguid = filters.get("orguid")
        print(visitid)
        print(orguid)
        # print(get_pipeline(visitid, orguid))
        cursor = list(collection.aggregate(get_pipeline(visitid, orguid)))
        print("here!")
        # or dynamic path
        file_path = f"patient_orders-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

        df = pd.DataFrame(list(cursor))
        print(list(cursor))
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Export Successful",
                            f"Data exported to {file_path}")

        # ✅ LOG SUCCESS
        # log_action(user, "EXPORT", {
        #     "filters": filters,
        #     "file": file_path,
        #     "status": "SUCCESS"
        # })

    except Exception as e:
        # ❗ LOG FAILURE
        # log_action(user, "EXPORT", {
        #     "filters": filters,
        #     "error": str(e),
        #     "status": "FAILED"
        # })

        raise e
