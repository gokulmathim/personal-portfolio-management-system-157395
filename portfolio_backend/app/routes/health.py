from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("Health", "health", url_prefix="/", description="Health check route")

@blp.route("/")
class HealthCheck(MethodView):
    """Health check endpoint."""

    # PUBLIC_INTERFACE
    @blp.doc(summary="Health check", description="Returns a simple health status payload.")
    def get(self):
        """Return simple health status."""
        return {"message": "Healthy"}
