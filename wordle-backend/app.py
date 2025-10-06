from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from models import db
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:5174"])

# Config
database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    # Fix for SQLAlchemy URL scheme change
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecret")

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    # Add default user for testing
    from models import User
    if not User.query.filter_by(username='testuser').first():
        hashed_pw = bcrypt.generate_password_hash('testpass').decode('utf-8')
        default_user = User(username='testuser', email='test@example.com', password_hash=hashed_pw)
        db.session.add(default_user)
        db.session.commit()

from routes.auth import auth_bp
from routes.game import game_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(game_bp, url_prefix="/game")

if __name__ == "__main__":
    app.run(debug=True)
