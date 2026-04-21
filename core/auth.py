ROLE_PERMISSIONS = {
    "IT-0003": ["export", "sbu_export"],
    "IT-0005": ["export", "users", "dashboard", "sbu_export"],
    # "manager": ["export", "dashboard"]
}


def has_permission(user, permission):
    for role in user["roles"]:
        if permission in ROLE_PERMISSIONS.get(role, []):
            return True
    return False
