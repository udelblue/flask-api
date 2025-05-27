from flask import Flask, Response, request, render_template, jsonify
import json
from pydantic import BaseModel
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

class Todo(BaseModel):
    id: int
    task: str

todos = [
    {"id": 1, "task": "Learn Flask"},
    {"id": 2, "task": "Build a web app"},
    {"id": 3, "task": "Deploy to production"}
]


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/api/todos", methods=["GET"])
def api_todos():

    return Response(response=json.dumps(todos), status=200, mimetype="application/json")
 
@app.route("/api/todos", methods=["POST"])
def api_add_todo():
    data = request.get_json()
    todo = Todo(**data)
    new_todo = {"id": len(todos) + 1, "task": todo.task}
    todos.append(new_todo)
    return Response(response=json.dumps(new_todo), status=201, mimetype="application/json")

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def api_delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return Response(status=204)


# Swagger documentation endpoint
@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Todo API"
    swag['info']['description'] = "API for managing todo items"
    return jsonify(swag)