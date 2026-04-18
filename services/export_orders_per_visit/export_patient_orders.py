from core.db import get_collection
import pandas as pd
from services.audit_service import log_action
from .mongo_query.pipeline import get_pipeline
from tkinter import messagebox
from datetime import datetime

# def export_to_csv(user, filters):


def export_patient_orders_to_csv(filters):
    try:
        collection = get_collection("patientorders")
        visitid = filters.get("visitid")
        orguid = filters.get("orguid")

        cursor = list(collection.aggregate(get_pipeline(visitid, orguid)))

        # or dynamic path
        file_path = f"patient_orders-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        if not list(cursor):
            return {"status": "empty"}

        df = pd.DataFrame(list(cursor))
        df["TotalPrice"] = pd.to_numeric(
            df["TotalPrice"], errors="coerce").fillna(0)
        # ✅ TOTAL NET AMOUNT (all)
        total_netamount = df["TotalPrice"].sum()

        # ✅ EXCLUDE cancelled / discontinued
        if "status" in df.columns:
            df_filtered = df[~df["StatusDesc"].str.lower().isin(
                ["Cancelled", "Discontinued"])]
        else:
            df_filtered = df

        total_netamount_valid = df_filtered["TotalPrice"].sum()

        df.to_csv(file_path, index=False)

        df = df.drop('PatientOrderID', axis=1)

        return {
            "status": "success",
            "file": file_path,
            "data": df,
            "total_netamount": total_netamount,
            "total_netamount_valid": total_netamount_valid
        }

    except Exception as e:

        raise e
