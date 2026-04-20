from .export_orders_per_visit.export_patient_orders import export_patient_orders_to_csv
from .export_user_login.export_login_users import export_login_users_to_csv
from .validate_user.validate_user import validate_user


def export_patient_orders(filters, callback):
    try:
        result = export_patient_orders_to_csv(filters)
        callback(result)

    except Exception as e:
        callback({"status": "error", "message": str(e)})


def export_login_users(filters, callback):

    try:
        result = export_login_users_to_csv(filters)
        callback(result)

    except Exception as e:
        callback({"status": "error", "message": str(e)})


def validate_user_login(filters):
    try:
        validate_user(filters)

    except Exception as e:
        raise e
