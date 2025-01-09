import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv



load_dotenv()
app = Flask(__name__)


# mongodb connection
mongo_url = os.getenv("MONGO_URI")
if not mongo_url:
    raise ValueError("mongo_uri environment variable not set")

client = MongoClient(mongo_url)
db = client["todo_db_python"]
todo_collection = db["todos"]




@app.route("/api/v1/todos", methods=["GET"])
def get_todos():
    filters = {}
    title = request.args.get("title")
    completed = request.args.get("completed")

    if title:
        filters["title"] = {"$regex": title, "$options": "i"}
    if completed is not None:
        filters["completed"] = completed.lower() == "true"

    todos = list(todo_collection.find(filters))
    for todo in todos:
        todo["_id"] = str(todo["_id"])

    return jsonify({"message": "todos fetched successfully", "data": todos}), 200




@app.route("/api/v1/todos", methods=["POST"])
def create_todo():
    data = request.json
    if not data or not "title" in data:
        return jsonify({"error": "title is required"}), 400

    new_todo = {
        "title": data["title"],
        "completed": data.get("completed", False),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    result = todo_collection.insert_one(new_todo)
    new_todo["_id"] = str(result.inserted_id)
    return jsonify({"message": "todo created successfully", "data": new_todo}), 201




@app.route("/api/v1/todos/<string:todo_id>", methods=["GET"])
def get_todo(todo_id):
    result = todo_collection.find_one({"_id": ObjectId(todo_id)})
    if not result:
        return jsonify({"error": "todo not found"}), 404

    result["_id"] = str(result["_id"])
    return jsonify({"message": "todo fetched successfully", "data": result}), 200




@app.route("/api/v1/todos/<string:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    if not data:
        return jsonify({"error": "request body is required"}), 400

    updated_todo = {}
    if "title" in data:
        updated_todo["title"] = data["title"]
    if "completed" in data:
        updated_todo["completed"] = data["completed"]

    updated_todo["updated_at"] = datetime.utcnow()

    result = todo_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": updated_todo})
    if result.matched_count == 0:
        return jsonify({"error": "todo not found"}), 404

    return jsonify({"message": "todo updated successfully"}), 200





@app.route("/api/v1/todos/<string:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    result = todo_collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "todo not found"}), 404

    return jsonify({"message": "todo deleted successfully"}), 200





if __name__ == "__main__":
    app.run(debug=True)
