
def update_to_ph_datetime(date_time):
    updated_date = {
        "$cond": {
            "if": {"$eq": [{"$type": date_time}, "date"]},
            "then":  {
                "$dateToString": {
                    "format": "%Y-%m-%d %H:%M:%S",
                    "date": date_time,
                    "timezone": "Asia/Manila"
                }
            },
            "else": None
        }
    }
    return updated_date
