from pydantic import BaseModel

from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI

info = Info(title="todo API", version="1.0.0")
app = OpenAPI(__name__, info=info)

todos_tag = Tag(name="todos", description="todos")


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





@app.get("/api/todos", summary="get books", tags=[todos_tag])
def api_todos():

    return Response(response=json.dumps(todos), status=200, mimetype="application/json")
 
@app.post("/api/todos", summary="post books", tags=[todos_tag])
def api_add_todo():
    data = request.get_json()
    todo = Todo(**data)
    new_todo = {"id": len(todos) + 1, "task": todo.task}
    todos.append(new_todo)
    return Response(response=json.dumps(new_todo), status=201, mimetype="application/json")


@app.delete("/api/todos/<int:todo_id>", summary="delete books", tags=[todos_tag])
def api_delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return Response(status=204)

if __name__ == "__main__":
    app.run(debug=True)