from core.task_queue import add_task
from services.export_service import (
    export_patient_orders, export_login_users, export_patient_charges)


# def export_data_async(user, filters):
#     add_task(export_to_csv, user, filters)


def export_data_async(filters, callback):
    add_task(export_patient_orders, filters, callback)


def export_data_async_patient_charges(filters, callback):
    add_task(export_patient_charges, filters, callback)


def export_data_async_login_users(filters, callback):
    add_task(export_login_users, filters, callback)
