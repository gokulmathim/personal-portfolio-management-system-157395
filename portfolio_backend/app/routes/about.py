from flask_smorest import Blueprint
from flask.views import MethodView
from ..schemas import AboutSchema, AboutUpdateSchema
from ..extensions import db
from ..models import AboutProfile
from ..utils.auth import admin_required

blp = Blueprint("About", "about", url_prefix="/about", description="About/Profile endpoints")

@blp.route("/")
class AboutSingle(MethodView):
    """Get or upsert the single About/Profile record."""

    # PUBLIC_INTERFACE
    @blp.response(200, AboutSchema)
    @blp.doc(summary="Get about", description="Get the single About/Profile record.")
    def get(self):
        about = AboutProfile.query.order_by(AboutProfile.id.asc()).first()
        if not about:
            about = AboutProfile()
            db.session.add(about)
            db.session.commit()
        return about

    # PUBLIC_INTERFACE
    @blp.arguments(AboutUpdateSchema)
    @blp.response(200, AboutSchema)
    @blp.doc(summary="Update about", description="Create or update the About/Profile record. Admin only.")
    @admin_required
    def put(self, payload):
        about = AboutProfile.query.order_by(AboutProfile.id.asc()).first()
        if not about:
            about = AboutProfile()
            db.session.add(about)
        for k, v in payload.items():
            setattr(about, k, v)
        db.session.commit()
        return about
