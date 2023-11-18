# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

@app.route('/')
def todo_list():
    with app.app_context():
        todos = Todo.query.all()
    return render_template('todo_list.html', todos=todos)

@app.route('/create', methods=['GET', 'POST'])
def todo_create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_todo = Todo(title=title, description=description)
        with app.app_context():
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for('todo_list'))
    return render_template('todo_form.html')

@app.route('/update/<int:todo_id>', methods=['GET', 'POST'])
def todo_update(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'POST':
        with app.app_context():
            todo.title = request.form['title']
            todo.description = request.form['description']
            db.session.merge(todo)
            db.session.commit()
        return redirect(url_for('todo_list'))
    return render_template('todo_form.html', todo=todo)

@app.route('/delete/<int:todo_id>')
def todo_delete(todo_id):
    with app.app_context():
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('todo_list'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
