from flask import Blueprint, request, jsonify, make_response
from .models import User
import bcrypt
import jwt
from datetime import datetime, timedelta
from config import JWT_KEY,default_profile_picture

auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
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
    except Exception as e:
        return jsonify({'message': 'interna server error', "error":str(e)}), 500


# Signup route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        if not request.form:
            return jsonify({'message': 'data is required'}), 400

        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({'message': 'all fields are required'}), 400

        if User.objects(username=username).first():
            return jsonify({'message': 'username already taken'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = User(
            username=username,
            password=hashed_password,
            profile_picture=default_profile_picture,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        new_user.save()

        return jsonify({'message': 'signup successful'}), 200
    except Exception as e:
        return jsonify({'message': 'interna server error', "error":str(e)}), 500
    

# Logout route
@auth_bp.route("/logout", methods=["POST"])
def logout():
    try:
        response = make_response(jsonify({"message": "logout successful"}))
        response.delete_cookie("hart")
        return response
    except Exception as e:
        return jsonify({"message": "internal server error", "error": str(e)}), 500
