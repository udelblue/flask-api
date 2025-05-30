from pydantic import BaseModel
from flask import Flask, Response, request, render_template, jsonify
import json
from flask_openapi3 import Info, Tag # type: ignore
from flask_openapi3 import OpenAPI # type: ignore

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


# API Setup
info = Info(title="todo API", version="1.0.0")
app = OpenAPI(__name__, info=info)
todos_tag = Tag(name="todos", description="todos")

# SQLAlchemy
# database connection URL (using SQLite in-memory database for simplicity)
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True) # echo=True logs SQL queries
Base = declarative_base()


# sqlalchemy models
class TodoModel(Base):
    __tablename__ = "todos"  # Table name

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)
    task = Column(String)
    completed = Column(Integer, default=0)  # 0 for not completed, 1 for complete

    def __repr__(self):
        return f"<Task(id={self.id}, owner='{self.owner}', task='{self.task}', completed={self.completed})>"

# Create the database tables (if they don't exist)
Base.metadata.create_all(bind=engine)
# Create a SessionLocal class to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# session to interact with the database
db = SessionLocal()



class Todo(BaseModel):
    id: int
    task: str

todos = [
    {"id": 1, "task": "Learn Flask"},
    {"id": 2, "task": "Build a web app"},
    {"id": 3, "task": "Deploy to production"}
]


# UI Endpoints

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

# API Endpoints

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