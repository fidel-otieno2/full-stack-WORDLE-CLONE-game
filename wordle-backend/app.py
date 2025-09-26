from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from models import db
from routes.auth import auth_bp
from routes.game import game_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(game_bp, url_prefix='/game')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
