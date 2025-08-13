from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .config import load_config
from .extensions import db, jwt
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.projects import blp as projects_blp
from .routes.blogs import blp as blogs_blp
from .routes.about import blp as about_blp
from .routes.contacts import blp as contacts_blp

# Expose the Api instance at module level so other modules (e.g., generate_openapi.py) can access the fully-registered spec.
api = None  # Will be initialized in create_app()

# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Flask: The configured Flask app instance with CORS, OpenAPI, JWT, DB, and routes.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Load configuration from environment variables (with safe fallbacks for development)
    load_config(app)

    # CORS configuration - allow all origins by default or restrict via env config
    CORS(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # OpenAPI/Swagger config
    app.config["API_TITLE"] = "Portfolio Backend API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config.setdefault("API_SPEC_OPTIONS", {})
    app.config["API_SPEC_OPTIONS"]["tags"] = [
        {"name": "Health", "description": "Health check route"},
        {"name": "Auth", "description": "Authentication endpoints for admin login and registration"},
        {"name": "Projects", "description": "CRUD operations for portfolio projects"},
        {"name": "Blogs", "description": "CRUD operations for blog posts"},
        {"name": "About", "description": "Profile/About information management"},
        {"name": "Contacts", "description": "Contact messages submission and admin review"},
    ]

    # Initialize extensions
    global api
    api = Api(app)
    db.init_app(app)
    jwt.init_app(app)

    # Create tables automatically if configured (default True for initial setup)
    if app.config.get("DB_AUTO_CREATE", True):
        with app.app_context():
            db.create_all()

    # Register blueprints
    api.register_blueprint(health_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(projects_blp)
    api.register_blueprint(blogs_blp)
    api.register_blueprint(about_blp)
    api.register_blueprint(contacts_blp)

    return app


# Create default app for run.py and openapi generation
app = create_app()
