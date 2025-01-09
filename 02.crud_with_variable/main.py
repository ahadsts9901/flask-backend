from flask import Flask, request, jsonify

app = Flask(__name__)

todos = []
next_id = 1



@app.route("/api/v1/todos", methods=["POST"])
def create_todo():
    global todos, next_id
    data = request.json
    if not data or not "title" in data:
        return jsonify({"error": "title is required"}), 400

    todo = {
        "id": next_id,
        "title": data["title"],
        "completed": data.get("completed", False),
    }
    todos.append(todo)
    next_id += 1
    return jsonify({"message": "todo created successfully", "data": todo}), 200




@app.route("/api/v1/todos", methods=["GET"])
def get_todos():
    completed_filter = request.args.get("completed")
    filtered_todos = todos
    if completed_filter is not None:
        filtered_todos = [
            todo for todo in todos if todo["completed"] == (completed_filter.lower() == "true")
        ]
    return jsonify({"message": "todos fetched successfully", "data": filtered_todos}), 200




@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "todo not found"}), 404
    return jsonify({"message": "todo fetched successfully", "data": todo}), 200




@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    global todos
    data = request.json
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "todo not found"}), 404

    todo["title"] = data.get("title", todo["title"])
    todo["completed"] = data.get("completed", todo["completed"])
    return jsonify({"message": "todo updated successfully", "data": todo}), 200




@app.route("/api/v1/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "todo not found"}), 404

    todos = [todo for todo in todos if todo["id"] != todo_id]
    return jsonify({"message": "todo deleted successfully"}), 200



if __name__ == "__main__":
    app.run(debug=True)

