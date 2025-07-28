from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.routes import bp as tasks_bp
    app.register_blueprint(tasks_bp)

    return app