from core.db import get_collection


def get_export_count():
    col = get_collection("audit_logs")
    return col.count_documents({"action": "EXPORT"})
