from flask import Flask, jsonify
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
# Allow your deployed frontend origin(s) (configurable)
cors_origins = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:3000",
]
CORS(app, origins=[o.strip() for o in cors_origins if o.strip()])


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

# --- Frontend (built React) serving ---
# If you run `npm run build` in `wordle-clone` and copy the generated files
# into `wordle-backend/static/`, this app will serve the SPA.
# React build output expected:
#   wordle-backend/static/assets/*
#   wordle-backend/static/index.html

from flask import send_from_directory, render_template


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(game_bp, url_prefix="/game")

# Serve React static files (if present)
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    # Backend routes should always win.
    if path.startswith("auth/") or path.startswith("game/"):
        return jsonify({"error": "Not found"}), 404

    # If a built file exists in static/, serve it.
    static_dir = os.path.join(app.root_path, "static")
    # Protect if static dir doesn't exist
    if os.path.isdir(static_dir):
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            # For SPA routes: always return index.html
            return send_from_directory(static_dir, "index.html")

    # Fallback template
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    # Bind to all interfaces for PaaS platforms
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1", host="0.0.0.0", port=port)

