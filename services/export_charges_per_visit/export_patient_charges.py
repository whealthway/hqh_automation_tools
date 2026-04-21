from core.db import get_collection
import pandas as pd
from services.audit_service import log_action
from .mongo_query.pipeline import get_pipeline
from tkinter import messagebox
from datetime import datetime

# def export_to_csv(user, filters):


def export_patient_charges_to_csv(filters):
    try:
        collection = get_collection("patientchargecodes")
        visitid = filters.get("visitid")
        orguid = filters.get("orguid")

        cursor = list(collection.aggregate(get_pipeline(visitid, orguid)))

        # or dynamic path
        file_path = f"patient_charges-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        if not list(cursor):
            return {"status": "empty"}

        df = pd.DataFrame(list(cursor))
        df["NetAmount"] = pd.to_numeric(
            df["NetAmount"], errors="coerce").fillna(0)

        df["StatusFlag"] = df["StatusFlag"].fillna("").str.upper()

        df_billed_amount = df[
            (df["StatusFlag"] == "A") & (df["IsBilled"] == True)
        ]["NetAmount"].sum()

        df_unbilled_amount = df[
            (df["StatusFlag"] == "A") & (
                (df["IsBilled"] == False) | (df["IsBilled"] == ""))
        ]["NetAmount"].sum()

        total_netamount = df[df["StatusFlag"] == "A"]["NetAmount"].sum()

        df.to_csv(file_path, index=False)

        df = df.drop('PatientOrderID', axis=1)

        return {
            "status": "success",
            "file": file_path,
            "data": df,
            "total_netamount": total_netamount,
            "df_billed_amount": df_billed_amount,
            "df_unbilled_amount": df_unbilled_amount,
        }

    except Exception as e:

        raise e
