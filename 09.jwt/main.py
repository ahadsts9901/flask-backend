import os
from flask import Flask, request, jsonify
from mongoengine import connect, Document, StringField, BooleanField, DateTimeField
from datetime import datetime
from dotenv import load_dotenv

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
    password = BooleanField(default=False)
    email = StringField(required=True,unique=True)
    profile_picture = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }



# login
@app.route("/api/v1/login", methods=["POST"])
def login():
    return jsonify({"message": "login successfully", "data": {}}), 200




# signup
@app.route("/api/v1/signup", methods=["POST"])
def login():
    return jsonify({"message": "signup successfully", "data": {}}), 200



# logout
@app.route("/api/v1/signup", methods=["POST"])
def login():
    return jsonify({"message": "signup successfully", "data": {}}), 200



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


