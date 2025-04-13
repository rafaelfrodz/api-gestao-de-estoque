from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.utils.errors import AuthenticationError

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        if not current_user_id:
            raise AuthenticationError()
        return f(*args, **kwargs)
    return decorated 