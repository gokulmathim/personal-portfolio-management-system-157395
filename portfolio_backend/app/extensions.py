from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# SQLAlchemy database instance
db = SQLAlchemy()

# JWT manager
jwt = JWTManager()
