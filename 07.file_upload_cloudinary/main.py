import os
from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),  # Replace with your Cloudinary cloud name
    api_key=os.getenv("CLOUDINARY_API_KEY"),       # Replace with your Cloudinary API key
    api_secret=os.getenv("CLOUDINARY_API_SECRET"), # Replace with your Cloudinary API secret
)


@app.route("/api/v1/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Upload the file to Cloudinary
        result = cloudinary.uploader.upload(file)

        # Return the URL of the uploaded file
        return jsonify({
            "message": "File uploaded successfully",
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "version": result["version"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
