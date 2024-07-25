from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.template_folder = 'templates'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add_todo():
    title = request.form["title"]
    todo = Todo(title=title)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<int:todo_id>")
def complete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    todo.completed = True
    todo.completed_at = datetime.now()
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/uncomplete/<int:todo_id>")
def uncomplete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    todo.completed = False
    todo.completed_at = None
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

def reset_database():
    db.drop_all()
    db.create_all()
    print("Database has been reset.")

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('todo.db'):
            db.create_all()
            print("Database created.")
        else:
            reset_database()
    
    app.run(host='0.0.0.0', port=8080, debug=True)
