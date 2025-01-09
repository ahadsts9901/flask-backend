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

connect("todo_db_python_schema", host=mongo_url)

# Define the Todo schema
class Todo(Document):
    title = StringField(required=True)
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@app.route("/api/v1/todos", methods=["GET"])
def get_todos():
    filters = {}
    title = request.args.get("title")
    completed = request.args.get("completed")

    if title:
        filters["title__icontains"] = title  # Case insensitive search
    if completed is not None:
        filters["completed"] = completed.lower() == "true"

    todos = Todo.objects(**filters)
    todos_list = [todo.to_dict() for todo in todos]

    return jsonify({"message": "todos fetched successfully", "data": todos_list}), 200


@app.route("/api/v1/todos", methods=["POST"])
def create_todo():
    data = request.json
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    new_todo = Todo(
        title=data["title"],
        completed=data.get("completed", False),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    new_todo.save()
    return jsonify({"message": "todo created successfully", "data": new_todo.to_dict()}), 201


@app.route("/api/v1/todos/<string:todo_id>", methods=["GET"])
def get_todo(todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        return jsonify({"message": "todo fetched successfully", "data": todo.to_dict()}), 200
    except Todo.DoesNotExist:
        return jsonify({"error": "todo not found"}), 404


@app.route("/api/v1/todos/<string:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    if not data:
        return jsonify({"error": "request body is required"}), 400

    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        return jsonify({"error": "todo not found"}), 404

    if "title" in data:
        todo.title = data["title"]
    if "completed" in data:
        todo.completed = data["completed"]

    todo.updated_at = datetime.utcnow()
    todo.save()

    return jsonify({"message": "todo updated successfully", "data": todo.to_dict()}), 200


@app.route("/api/v1/todos/<string:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return jsonify({"message": "todo deleted successfully"}), 200
    except Todo.DoesNotExist:
        return jsonify({"error": "todo not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
