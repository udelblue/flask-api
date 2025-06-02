from pydantic import BaseModel
from flask import Flask, Response, request, render_template, jsonify
import json
from flask_openapi3 import Info, Tag # type: ignore
from flask_openapi3 import OpenAPI # type: ignore
from flask_openapi3 import APIBlueprint # type: ignore

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
class Todo(Base):
    __tablename__ = "todos"  # Table name

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)
    task = Column(String)
    priority = Column(Integer, default=0)  # Default priority is 
    completed = Column(Integer, default=0)  # 0 for not completed, 1 for complete
    due_date = Column(String, nullable=True)  # Optional due date

    def __repr__(self):
        return f"<Task(id={self.id}, owner='{self.owner}', task='{self.task}', completed={self.completed})>"

# Create the database tables (if they don't exist)
Base.metadata.create_all(bind=engine)
# Create a SessionLocal class to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# session to interact with the database
db = SessionLocal()



class TodoSchema(BaseModel):
    id: int
    task: str
    priority: int = 0
    completed: int = 0
    due_date: str | None = None


# UI Endpoints

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

# API todos Endpoints


todos_api = APIBlueprint('todos', __name__, url_prefix='/api/todos', abp_tags=[todos_tag])

@todos_api.get('/')
def get_todos():
    todos = db.query(Todo).all()
    return jsonify([TodoSchema(
        id=getattr(todo, "id"),
        task=str(getattr(todo, "task")),
        priority=getattr(todo, "priority"),
        completed=getattr(todo, "completed"),
        due_date=str(getattr(todo, "due_date"))
    ).dict() for todo in todos])

@todos_api.get('/<int:todo_id>')
def get_todo_by_id(todo_id):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(TodoSchema(
        id=getattr(todo, "id"),
        task=str(getattr(todo, "task")),
        priority=getattr(todo, "priority"),
        completed=getattr(todo, "completed"),
        due_date=str(getattr(todo, "due_date"))
    ).dict())

@todos_api.post('/')
def create_todo():
    data = request.json
    todo_data = TodoSchema(**data)
    todo = Todo(
        id=todo_data.id,
        task=todo_data.task,
        priority=todo_data.priority,
        completed=todo_data.completed,
        due_date=todo_data.due_date,
        owner="default"
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return jsonify(TodoSchema(
        id=getattr(todo, "id"),
        task=str(getattr(todo, "task")),
        priority=getattr(todo, "priority"),
        completed=getattr(todo, "completed"),
        due_date=str(getattr(todo, "due_date"))
    ).dict()), 201

@todos_api.put('/<int:todo_id>')
def update_todo(todo_id):
    data = request.json
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    todo_data = TodoSchema(id=todo.id, **data)
    todo.task = todo_data.task
    todo.priority = todo_data.priority
    todo.completed = todo_data.completed
    todo.due_date = todo_data.due_date
    db.commit()
    db.refresh(todo)
    return jsonify(TodoSchema(
        id=getattr(todo, "id"),
        task=str(getattr(todo, "task")),
        priority=getattr(todo, "priority"),
        completed=getattr(todo, "completed"),
        due_date=str(getattr(todo, "due_date"))
    ).dict())

@todos_api.delete('/<int:todo_id>')
def delete_todo(todo_id):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.delete(todo)
    db.commit()
    return jsonify({"message": "Todo deleted"})



app.register_api(todos_api)



# Health Check Endpoint
health_api = APIBlueprint('health', __name__, url_prefix='/api/health')
@health_api.get('/')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200
app.register_api(health_api)



# Entry point for the application
if __name__ == "__main__":
    app.run(debug=True)