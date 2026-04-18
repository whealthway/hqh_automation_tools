from services.user_service import authenticate_user, authenticate_user_verification_code


def login_user(username, password):
    """
    Handles login request from UI
    """
    user_data = authenticate_user(username, password)

    if not user_data:
        return None

    return user_data


def verify_code(username, code):
    is_code_verified = authenticate_user_verification_code(username, code)

    return is_code_verified
