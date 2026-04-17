
from .projection import User


def get_pipeline(loginid):
    return [
        {
            "$match": {"loginid": loginid}
        },
        {
            '$project': User
        },
    ]
