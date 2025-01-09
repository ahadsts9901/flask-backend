import os
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("simple-database-b15ab-firebase-adminsdk-vbe7e-2c49ecc0e9.json")  # Replace with your service account key path
firebase_bucket = os.getenv("FIREBASE_BUCKET")
firebase_admin.initialize_app(cred, {
    "storageBucket": firebase_bucket  # Replace with your Firebase Storage bucket URL
})

# Firebase storage bucket
bucket = storage.bucket()


@app.route("/api/v1/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Create a blob in the bucket
        blob = bucket.blob(file.filename)

        # Upload the file to Firebase Storage
        blob.upload_from_file(file)

        # Optionally, make the file public and get its URL
        blob.make_public()
        file_url = blob.public_url

        return jsonify({"message": "File uploaded successfully", "url": file_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
