from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from ..schemas import ContactCreateSchema, ContactSchema
from ..extensions import db
from ..models import ContactMessage
from ..utils.auth import admin_required

blp = Blueprint("Contacts", "contacts", url_prefix="/contacts", description="Contact message endpoints")

def _paginate(query):
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 20)), 100)
    return query.paginate(page=page, per_page=per_page, error_out=False)

@blp.route("/")
class ContactsCollection(MethodView):
    """Submit or list contact messages."""

    # PUBLIC_INTERFACE
    @blp.arguments(ContactCreateSchema)
    @blp.response(201, ContactSchema)
    @blp.doc(summary="Submit contact", description="Submit a contact message (public).")
    def post(self, payload):
        msg = ContactMessage(**payload)
        db.session.add(msg)
        db.session.commit()
        return msg, 201

    # PUBLIC_INTERFACE
    @blp.response(200, ContactSchema(many=True))
    @blp.doc(summary="List contacts", description="List contact messages (admin only).")
    @admin_required
    def get(self):
        pagination = _paginate(ContactMessage.query.order_by(ContactMessage.created_at.desc()))
        return pagination.items

@blp.route("/<int:message_id>")
class ContactItem(MethodView):
    """Get or delete a contact message by id."""

    # PUBLIC_INTERFACE
    @blp.response(200, ContactSchema)
    @blp.doc(summary="Get contact", description="Get a single contact message (admin only).")
    @admin_required
    def get(self, message_id: int):
        msg = ContactMessage.query.get_or_404(message_id)
        return msg

    # PUBLIC_INTERFACE
    @blp.doc(summary="Delete contact", description="Delete a contact message (admin only).")
    @admin_required
    def delete(self, message_id: int):
        msg = ContactMessage.query.get_or_404(message_id)
        db.session.delete(msg)
        db.session.commit()
        return {"message": "Deleted"}, 200
