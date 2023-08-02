from flask import Flask, render_template, redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
db.init_app(app)
app.app_context().push()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)

@app.route("/")
def index():
    todo_list = Todo.query.all()
    total_todo = Todo.query.count()
    return render_template ("dashboard/index.html", todo_list = todo_list, total_todo = total_todo )

@app.route("/add", methods=['POST'])
def add():
    #//title// is the title in class //form-control// in the //Index// File
    title = request.form.get("title")
    new_todo= Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:id>")
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template ("dashboard/about.html")

#new day new Projx
if __name__ == '__main__':
    app.run(debug=True)