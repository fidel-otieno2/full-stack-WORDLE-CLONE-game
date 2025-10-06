from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from flask_bcrypt import bcrypt
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username taken'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email taken'}), 400

    hashed = bcrypt.generate_password_hash(password)
    user = User(username=username, email=email, password_hash=hashed)
    db.session.add(user)
    db.session.commit()

    # After commit, user.id is set
    token = create_access_token(identity=user.id)
    return jsonify({'token': token, 'message': 'User registered'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'token': token}), 200
