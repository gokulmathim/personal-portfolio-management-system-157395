from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from ..schemas import ProjectSchema, ProjectCreateSchema, ProjectUpdateSchema
from ..extensions import db
from ..models import Project
from ..utils.auth import admin_required

blp = Blueprint("Projects", "projects", url_prefix="/projects", description="Project CRUD endpoints")

def _paginate(query):
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 20)), 100)
    return query.paginate(page=page, per_page=per_page, error_out=False)

@blp.route("/")
class ProjectsCollection(MethodView):
    """List and create projects."""

    # PUBLIC_INTERFACE
    @blp.response(200, ProjectSchema(many=True))
    @blp.doc(summary="List projects", description="Fetch a paginated list of projects.")
    def get(self):
        """Return a list of projects (public)."""
        pagination = _paginate(Project.query.order_by(Project.created_at.desc()))
        return pagination.items

    # PUBLIC_INTERFACE
    @blp.arguments(ProjectCreateSchema)
    @blp.response(201, ProjectSchema)
    @blp.doc(summary="Create project", description="Create a new project. Admin only.")
    @admin_required
    def post(self, payload):
        """Create a new project (admin only)."""
        proj = Project(
            title=payload["title"],
            description=payload.get("description"),
            url=payload.get("url"),
            tags=payload.get("tags"),
            is_featured=payload.get("is_featured", False),
        )
        db.session.add(proj)
        db.session.commit()
        return proj, 201

@blp.route("/<int:project_id>")
class ProjectItem(MethodView):
    """Retrieve, update, and delete a project."""

    # PUBLIC_INTERFACE
    @blp.response(200, ProjectSchema)
    @blp.doc(summary="Get project", description="Get a project by ID.")
    def get(self, project_id: int):
        """Fetch single project (public)."""
        proj = Project.query.get_or_404(project_id)
        return proj

    # PUBLIC_INTERFACE
    @blp.arguments(ProjectUpdateSchema)
    @blp.response(200, ProjectSchema)
    @blp.doc(summary="Update project", description="Update a project by ID. Admin only.")
    @admin_required
    def put(self, payload, project_id: int):
        """Update a project (admin only)."""
        proj = Project.query.get_or_404(project_id)
        for k, v in payload.items():
            setattr(proj, k, v)
        db.session.commit()
        return proj

    # PUBLIC_INTERFACE
    @blp.doc(summary="Delete project", description="Delete a project by ID. Admin only.")
    @admin_required
    def delete(self, project_id: int):
        """Delete a project (admin only)."""
        proj = Project.query.get_or_404(project_id)
        db.session.delete(proj)
        db.session.commit()
        return {"message": "Deleted"}, 200
