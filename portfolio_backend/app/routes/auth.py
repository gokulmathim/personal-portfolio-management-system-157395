from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from flask_jwt_extended import create_access_token
from ..schemas import LoginSchema, RegisterSchema, TokenSchema
from ..extensions import db
from ..models import AdminUser
import os

blp = Blueprint("Auth", "auth", url_prefix="/auth", description="Authentication endpoints")

@blp.route("/login")
class AuthLogin(MethodView):
    """Admin login endpoint."""

    # PUBLIC_INTERFACE
    @blp.arguments(LoginSchema)
    @blp.response(200, TokenSchema)
    @blp.doc(summary="Admin login", description="Authenticate an admin and return a JWT access token.")
    def post(self, credentials):
        """Login with username and password, returning a JWT token."""
        username = credentials["username"]
        password = credentials["password"]
        user = AdminUser.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {"message": "Invalid username or password"}, 401
        access_token = create_access_token(identity=user.id, additional_claims={"is_admin": True})
        return {"access_token": access_token, "token_type": "bearer"}

@blp.route("/register")
class AuthRegister(MethodView):
    """Admin registration endpoint guarded by token."""

    # PUBLIC_INTERFACE
    @blp.arguments(RegisterSchema)
    @blp.response(201, TokenSchema)
    @blp.doc(
        summary="Register admin",
        description="Register a new admin user if ADMIN_REGISTRATION_TOKEN is set and provided via 'X-Admin-Token' header."
    )
    def post(self, payload):
        """Register a new admin user if the correct registration token is provided in headers."""
        reg_token_required = os.getenv("ADMIN_REGISTRATION_TOKEN")
        if not reg_token_required:
            return {"message": "Registration disabled. Set ADMIN_REGISTRATION_TOKEN to enable."}, 403

        header_token = request.headers.get("X-Admin-Token")
        if not header_token or header_token != reg_token_required:
            return {"message": "Forbidden"}, 403

        username = payload["username"]
        password = payload["password"]
        if AdminUser.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 409

        user = AdminUser(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id, additional_claims={"is_admin": True})
        return {"access_token": access_token, "token_type": "bearer"}, 201
