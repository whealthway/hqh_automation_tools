from services.user_service import authenticate_user
from models.user import User


def login_user(username, password):
    """
    Handles login request from UI
    """
    user_data = authenticate_user(username, password)

    if not user_data:
        return None

    # Convert dict → User model
    user = User(
        username=user_data["username"],
        roles=user_data.get("roles", [])
    )

    return user
