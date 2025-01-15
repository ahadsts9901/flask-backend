from flask import Flask
from auth_routes import auth_bp
from user_routes import user_bp
from admin_routes import admin_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints for different routes
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    return app
