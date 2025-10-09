from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from extensions import bcrypt
from dotenv import load_dotenv
import os
from models import db
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "https://full-stack-wordle-clone-game.vercel.app", "http://localhost:3000"])

# Config - Use PostgreSQL with Supabase credentials from environment variables
database_url = os.getenv("DATABASE_URL")
if database_url:
    try:
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        if "+" not in database_url:
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        if "?sslmode=" not in database_url:
            database_url += "?sslmode=require"
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    except Exception as e:
        print(f"Error parsing DATABASE_URL: {e}, falling back to SQLite")
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecret")

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# The databse set up
with app.app_context(): 
    db.create_all()

from routes.auth import auth_bp
from routes.game import game_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(game_bp, url_prefix="/game")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
