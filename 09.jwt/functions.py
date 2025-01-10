import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

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
