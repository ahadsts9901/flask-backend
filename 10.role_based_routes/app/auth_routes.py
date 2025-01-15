from flask import Blueprint, request, jsonify, make_response
from .models import User
import bcrypt
import jwt
from datetime import datetime, timedelta
from .config import JWT_KEY

auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'username and password are required'}), 400

    username = data['username']
    password = data['password']

    user = User.objects(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'message': 'username or password incorrect'}), 400

    payload = {
        'id': str(user.id),
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, JWT_KEY, algorithm="HS256")
    response = make_response(jsonify({'message': 'login successful'}))
    response.set_cookie('hart', token, httponly=True, secure=True)

    return response

# Signup route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    if not request.form or not request.files:
        return jsonify({'message': 'form data and file are required'}), 400

    username = request.form.get('username')
    password = request.form.get('password')
    profile_picture = request.files.get('file')

    if not username or not password or not profile_picture:
        return jsonify({'message': 'all fields are required'}), 400

    if User.objects(username=username).first():
        return jsonify({'message': 'username already taken'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = User(
        username=username,
        password=hashed_password,
        role='user',  # Default role
        profile_picture='profile_picture_url',  # For simplicity; you'd save the image
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    new_user.save()

    return jsonify({'message': 'signup successful'}), 200
