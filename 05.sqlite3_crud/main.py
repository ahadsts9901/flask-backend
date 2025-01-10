import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# database setup
DB_FILE = "sqlite_3_todos.db"

def init_db():
    # initialize the database with the todos table
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)
        conn.commit()

init_db()

def query_db(query, args=(), one=False):
    # helper function to query the database
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv


# api endpoints

@app.route("/api/v1/todos", methods=["GET"])
def get_todos():
    # fetch all todos with optional filters
    title = request.args.get("title")
    completed = request.args.get("completed")

    query = "SELECT * FROM todos WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
    if completed is not None:
        query += " AND completed = ?"
        params.append(1 if completed.lower() == "true" else 0)

    todos = query_db(query, params)
    todos_list = [dict(todo) for todo in todos]

    return jsonify({"message": "todos fetched successfully", "data": todos_list}), 200


@app.route("/api/v1/todos", methods=["POST"])
def create_todo():
    # create a new todo
    data = request.json
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    created_at = updated_at = datetime.now().isoformat()
    query = """
        INSERT INTO todos (title, completed, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    """
    params = (data["title"], data.get("completed", False), created_at, updated_at)
    todo_id = query_db(query, params)
    new_todo = {
        # "id": todo_id.lastrowid,
        "title": data["title"],
        "completed": data.get("completed", False),
        "created_at": created_at,
        "updated_at": updated_at,
    }
    return jsonify({"message": "todo created successfully", "data": new_todo}), 201


@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    # fetch a single todo by id
    todo = query_db("SELECT * FROM todos WHERE id = ?", (todo_id,), one=True)
    if not todo:
        return jsonify({"error": "todo not found"}), 404

    return jsonify({"message": "todo fetched successfully", "data": dict(todo)}), 200


@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = query_db("SELECT * FROM todos WHERE id = ?", (todo_id,), one=True)
    if not todo:
        return jsonify({"error": "todo not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "request body is required"}), 400

    fields = []
    params = []

    if "title" in data:
        fields.append("title = ?")
        params.append(data["title"])
    if "completed" in data:
        fields.append("completed = ?")
        params.append(1 if data["completed"] else 0)

    params.append(datetime.now().isoformat())  # updated_at
    params.append(todo_id)

    query = f"UPDATE todos SET {', '.join(fields)}, updated_at = ? WHERE id = ?"
    query_db(query, params)

    return jsonify({"message": "todo updated successfully"}), 200


@app.route("/api/v1/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = query_db("SELECT * FROM todos WHERE id = ?", (todo_id,), one=True)
    if not todo:
        return jsonify({"error": "todo not found"}), 404

    query_db("DELETE FROM todos WHERE id = ?", (todo_id,))
    return jsonify({"message": "todo deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
