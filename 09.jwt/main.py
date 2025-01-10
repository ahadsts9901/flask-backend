import os
import bcrypt
import jwt
from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
from mongoengine import connect, Document, StringField, BooleanField, DateTimeField
from datetime import datetime
from dotenv import load_dotenv
from functions import upload_profile_picture

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection setup using MongoEngine
mongo_url = os.getenv("MONGO_URI")
if not mongo_url:
    raise ValueError("mongo_uri environment variable not set")

connect("jwt_flask_python", host=mongo_url)

# Define the User schema
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



# login
@app.route("/api/v1/login", methods=["POST"])
def login():
    print("hello")
    data = request.json
    if not data:
        return jsonify({"message": "data is required"}), 400
    if not "username" in data:
        return jsonify({"message": "username is required"}), 400

    if not "password" in data:
        return jsonify({"message": "password is required"}), 400

    username = data["username"]
    password = data["password"]

    user_exist = User.objects(username=username).first()
    if not user_exist:
        return jsonify({"message": "username or password incorrect"}), 400

    is_password_correct = bcrypt.checkpw(password.encode("utf-8"), user_exist["password"].encode("utf-8"))
    
    if not is_password_correct:
        return jsonify({"message": "username or password incorrect"}), 400

    payload = {
        "id": str(user_exist["id"]),
        "username": user_exist["username"],
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expiry in 1 hour
    }

    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Create response and set JWT in cookies
    response = make_response(jsonify({"message": "login successful"}))
    response.set_cookie(
        "hart", 
        token, 
        httponly=True,  # Make the cookie inaccessible via JavaScript
        secure=True,    # Use secure flag for HTTPS
        samesite="Strict"  # Prevent CSRF attacks
    )
    
    return response



# signup
@app.route("/api/v1/signup", methods=["POST"])
def signup():
    if not request.form or not request.files:
        return jsonify({"message": "Form data and file are required"}), 400

    username = request.form.get("username")
    password = request.form.get("password")
    profile_picture = request.files.get("file")

    if not username:
        return jsonify({"message": "username is required"}), 400
    if not password:
        return jsonify({"message": "password is required"}), 400
    if not profile_picture:
        return jsonify({"message": "profile picture is required"}), 400

    user_exist = User.objects(username=username).first()
    if user_exist:
        return jsonify({"message": "username already taken"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    password = hashed_password.decode("utf-8")
    profile_url = upload_profile_picture(profile_picture)

    new_user = User(
        username=username,
        password=password,
        profile_picture=str(profile_url["url"]),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    new_user.save()

    return jsonify({"message": "signup successful"}), 200




# logout
@app.route("/api/v1/logout", methods=["POST"])
def logout():
    return jsonify({"message": "logout successfully", "data": {}}), 200



# get current user profile
@app.route("/api/v1/profile", methods=["GET"])
def get_current_user_profile(): 
    return jsonify({"message": "current user profile fetched", "data": {}}), 200



# get user profile
@app.route("/api/v1/profile/<string:user_id>", methods=["GET"])
def get_user_profile(user_id):
    return jsonify({"message": "user profile fetched", "data": {}}), 404



# protected_route
@app.route("/api/v1/protected", methods=["GET"])
def protected():
    return jsonify({"message": "protected route fetched", "data": {}}), 404



if __name__ == "__main__":
    app.run(debug=True)


