import os
import cloudinary
import cloudinary.uploader
import jwt
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv()
JWT_KEY = os.getenv("JWT_KEY")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

def upload_profile_picture(file):
    if  not file:
        return {"message": "file is required"}

    if file.filename == "":
        return {"message": "file is required"}

    try:
        result = cloudinary.uploader.upload(file)

        return {
            "message": "File uploaded successfully",
            "url": result["secure_url"]
        }

    except Exception as e:
        return {"message": "something went wrong", "error": str(e)}


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("hart")
        
        if not token:
            return jsonify({"message": "unauthorized"}), 401

        try:
            payload = jwt.decode(token, JWT_KEY, algorithms=["HS256"])
            request.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function
