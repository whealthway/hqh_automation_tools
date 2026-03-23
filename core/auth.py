ROLE_PERMISSIONS = {
    "corp": ["export", "users", "dashboard", "sbu_export"],
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
