ROLE_PERMISSIONS = {
    "IT-0003": ["export", "users", "dashboard", "sbu_export"],
    "IT-0005": ["export", "users", "dashboard", "sbu_export"],
    "sbu": ["sbu_export"],
    # "manager": ["export", "dashboard"]
}


def has_permission(user, permission):
    print(f"auth: {user}")
    for role in user["roles"]:
        print(role)
        print(ROLE_PERMISSIONS.get(role, []))
        if permission in ROLE_PERMISSIONS.get(role, []):
            return True
    return False
