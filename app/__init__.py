import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate  # Import Migrate

# === Initialize extensions ===
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()  # Initialize Migrate

# === Base directory ===
basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)

    # === Configuration ===
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure secret
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, '..', 'uploads')

    # Create upload folder if not exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # === Initialize extensions ===
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate with the app and db

    # Login manager config
    login_manager.login_view = 'routes.login'
    login_manager.login_message_category = 'info'

    # === Register Blueprints ===
    from app.routes import routes
    app.register_blueprint(routes)

    return app
