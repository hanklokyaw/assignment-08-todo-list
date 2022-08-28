from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_gravatar import Gravatar
import datetime

app = Flask(__name__)

Bootstrap(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

today = datetime.datetime.today().strftime('%d/%m/%Y')

##CONFIGURE TABLES

class Todo(db.Model):
    __tablename__ = "todo_list"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    progress = db.Column(db.Boolean, default=False, nullable=False)
db.create_all()
# db.drop_all()

@app.route('/', methods=["GET", "POST"])
def get_all_tasks():
    tasks = Todo.query.all()
    if request.method == 'POST':
        print(request.form['new_task'])
        new_task = Todo(title=request.form['new_task'])
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("get_all_tasks"))
    return render_template("index.html", all_tasks=tasks, today=today)


@app.route("/task/<int:task_id>")
def show_task(task_id):
    requested_task = Todo.query.get(task_id)
    return render_template("post.html", task=requested_task)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task_to_delete = Todo.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_tasks'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
