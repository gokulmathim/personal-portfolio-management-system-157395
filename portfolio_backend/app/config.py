import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from a .env file if present (development)
load_dotenv()

# PUBLIC_INTERFACE
def load_config(app) -> None:
    """Load configuration into the Flask app from environment variables.

    Environment variables:
        DATABASE_URL: Full database URL (preferred). Example: postgresql+psycopg2://user:pass@host:5432/dbname
        POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD: Used if DATABASE_URL not provided.
        JWT_SECRET_KEY: Secret key for JWT token signing.
        CORS_ORIGINS: Comma-separated origins allowed for CORS.
        DB_AUTO_CREATE: 'true' to auto-create tables on startup (default true).
        DEBUG: 'true' to enable debug.
    """
    app.config["DEBUG"] = os.getenv("DEBUG", "false").lower() == "true"

    # Database
    db_url = _get_database_url_from_env()
    if not db_url:
        raise RuntimeError(
            "Database configuration missing. Provide DATABASE_URL or POSTGRES_* variables."
        )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if not jwt_secret:
        raise RuntimeError("JWT_SECRET_KEY environment variable is required.")
    app.config["JWT_SECRET_KEY"] = jwt_secret

    # CORS
    cors_origins = os.getenv("CORS_ORIGINS", "*")
    app.config["CORS_ORIGINS"] = [o.strip() for o in cors_origins.split(",")] if cors_origins else "*"

    # Auto-create
    app.config["DB_AUTO_CREATE"] = os.getenv("DB_AUTO_CREATE", "true").lower() == "true"


def _get_database_url_from_env() -> Optional[str]:
    """Build a SQLAlchemy database URL from environment variables if needed."""
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url

    host = os.getenv("POSTGRES_HOST")
    db = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    port = os.getenv("POSTGRES_PORT", "5432")
    if host and db and user and password:
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return None
