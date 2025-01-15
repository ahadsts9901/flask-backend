import os
import bcrypt
import jwt
from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
from mongoengine import connect, Document, StringField, BooleanField, DateTimeField
from dotenv import load_dotenv
from functions import upload_profile_picture, jwt_required

load_dotenv()

app = Flask(__name__)

JWT_KEY = os.getenv("JWT_KEY")

# connect to mongodb
mongo_url = os.getenv("MONGO_URI")
if not mongo_url:
    raise ValueError("mongo_uri environment variable not set")

connect("jwt_flask_python", host=mongo_url)

# user schema
class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    profile_picture = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "password": self.password,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

# login route
@app.route("/api/v1/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "data is required"}), 400
        if "username" not in data or "password" not in data:
            return jsonify({"message": "username and password are required"}), 400

        username = data["username"]
        password = data["password"]

        user = User.objects(username=username).first()
        if not user:
            return jsonify({"message": "username or password incorrect"}), 400

        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return jsonify({"message": "username or password incorrect"}), 400

        payload = {
            "id": str(user.id),
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }

        token = jwt.encode(payload, JWT_KEY, algorithm="HS256")
        response = make_response(jsonify({"message": "login successful"}))
        response.set_cookie("hart", token, httponly=True, secure=True)
        return response

    except Exception as e:
        return jsonify({"message": "internal server error", "error": str(e)}), 500

# signup route
@app.route("/api/v1/signup", methods=["POST"])
def signup():
    try:
        if not request.form or not request.files:
            return jsonify({"message": "form data and file are required"}), 400

        username = request.form.get("username")
        password = request.form.get("password")
        profile_picture = request.files.get("file")

        if not username or not password or not profile_picture:
            return jsonify({"message": "all fields are required"}), 400

        if User.objects(username=username).first():
            return jsonify({"message": "username already taken"}), 400

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        profile_url = upload_profile_picture(profile_picture)

        new_user = User(
            username=username,
            password=hashed_password,
            profile_picture=profile_url["url"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        new_user.save()

        return jsonify({"message": "signup successful"}), 200

    except Exception as e:
        return jsonify({"message": "internal server error", "error": str(e)}), 500

# logout route
@app.route("/api/v1/logout", methods=["POST"])
def logout():
    try:
        response = make_response(jsonify({"message": "logout successful"}))
        response.delete_cookie("hart")
        return response
    except Exception as e:
        return jsonify({"message": "internal server error", "error": str(e)}), 500

# get current user profile route
@app.route("/api/v1/profile", methods=["GET"])
@jwt_required
def get_current_user_profile():
    try:
        user_id = request.current_user["id"]
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"message": "user not found"}), 404

        return jsonify({
            "message": "current user profile fetched",
            "data": {
                "id": str(user.id),
                "username": user.username,
                "profile_picture": user.profile_picture,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "invalid token"}), 401
    except Exception as e:
        return jsonify({"message": "internal server error", "error": str(e)}), 500

# protected route
@app.route("/api/v1/protected", methods=["GET"])
@jwt_required
def protected():
    try:
        return jsonify({"message": "protected route accessed"}), 200
    except Exception as e:
        return jsonify({"message": "internal server error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
