from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

# PUBLIC_INTERFACE
def admin_required(fn):
    """Decorator to require JWT with is_admin claim.

    Returns 403 if token is missing the is_admin claim or not truthy.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt() or {}
        if not claims.get("is_admin"):
            return jsonify({"message": "Admin privileges required"}), 403
        return fn(*args, **kwargs)
    return wrapper
