from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from ..schemas import BlogSchema, BlogCreateSchema, BlogUpdateSchema
from ..extensions import db
from ..models import BlogPost
from ..utils.auth import admin_required

blp = Blueprint("Blogs", "blogs", url_prefix="/blogs", description="Blog posts CRUD endpoints")

def _paginate(query):
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 20)), 100)
    # Flask-SQLAlchemy 3.x: use db.paginate instead of Query.paginate
    return db.paginate(query, page=page, per_page=per_page, error_out=False)

@blp.route("/")
class BlogCollection(MethodView):
    """List and create blog posts."""

    # PUBLIC_INTERFACE
    @blp.response(200, BlogSchema(many=True))
    @blp.doc(summary="List blogs", description="Fetch a paginated list of blogs. Public or published.")
    def get(self):
        """List public blogs."""
        query = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc())
        pagination = _paginate(query)
        return pagination.items

    # PUBLIC_INTERFACE
    @blp.arguments(BlogCreateSchema)
    @blp.response(201, BlogSchema)
    @blp.doc(summary="Create blog", description="Create a new blog post. Admin only.")
    @admin_required
    def post(self, payload):
        """Create blog (admin)."""
        post = BlogPost(**payload)
        db.session.add(post)
        db.session.commit()
        return post, 201

@blp.route("/all")
class BlogAll(MethodView):
    """Admin listing of all blogs regardless of published state."""

    # PUBLIC_INTERFACE
    @blp.response(200, BlogSchema(many=True))
    @blp.doc(summary="List all blogs", description="List all blogs (admin only).")
    @admin_required
    def get(self):
        return BlogPost.query.order_by(BlogPost.created_at.desc()).all()

@blp.route("/<int:blog_id>")
class BlogItem(MethodView):
    """Get, update, delete a blog post."""

    # PUBLIC_INTERFACE
    @blp.response(200, BlogSchema)
    @blp.doc(summary="Get blog", description="Get a blog post by ID. Unpublished posts require admin.")
    def get(self, blog_id: int):
        """Fetch a blog post by ID. If the post is unpublished, admin privileges are required."""
        post = BlogPost.query.get_or_404(blog_id)
        # If the post is not published, require an admin JWT
        if not post.is_published:
            try:
                from flask_jwt_extended import verify_jwt_in_request, get_jwt
                verify_jwt_in_request()
                claims = get_jwt() or {}
                if not claims.get("is_admin"):
                    return {"message": "Admin privileges required"}, 403
            except Exception:
                return {"message": "Admin privileges required"}, 403
        return post

    # PUBLIC_INTERFACE
    @blp.arguments(BlogUpdateSchema)
    @blp.response(200, BlogSchema)
    @blp.doc(summary="Update blog", description="Update a blog post (admin only).")
    @admin_required
    def put(self, payload, blog_id: int):
        post = BlogPost.query.get_or_404(blog_id)
        for k, v in payload.items():
            setattr(post, k, v)
        db.session.commit()
        return post

    # PUBLIC_INTERFACE
    @blp.doc(summary="Delete blog", description="Delete a blog post (admin only).")
    @admin_required
    def delete(self, blog_id: int):
        post = BlogPost.query.get_or_404(blog_id)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Deleted"}, 200

@blp.route("/slug/<string:slug>")
class BlogBySlug(MethodView):
    """Get blog post by slug (public for published)."""

    # PUBLIC_INTERFACE
    @blp.response(200, BlogSchema)
    @blp.doc(summary="Get blog by slug", description="Get a blog post by slug if published.")
    def get(self, slug: str):
        post = BlogPost.query.filter_by(slug=slug, is_published=True).first()
        if not post:
            return {"message": "Not found"}, 404
        return post
