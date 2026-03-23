from .export_orders_per_visit.export_patient_orders import export_to_csv


def export_patient_orders(filters):
    try:
        export_to_csv(filters)

    except Exception as e:
        raise e
