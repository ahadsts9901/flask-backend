from flask import Flask
from mongoengine import connect
from .auth_routes import auth_bp
from .user_routes import user_bp
from .admin_routes import admin_bp
from config import MONGO_URI

def create_app():
    app = Flask(__name__)

    if not MONGO_URI:
        raise ValueError("mongo_uri environment variable not set")

    connect("roles_pflask_schema", host=MONGO_URI)

    # Register blueprints for different routes
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    return app
