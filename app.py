from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from data import db_session
from data.all_models import Todo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'todo'
db = SQLAlchemy(app)


def main():
    db_session.global_init("db/todo.db")
    app.run(port=8000)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    t = db_sess.query(Todo).all()
    return render_template('table.html', data=t)


@app.route('/change/<id>', methods=["GET"])
def change(id):
    db_sess = db_session.create_session()
    t = db_sess.query(Todo).filter(Todo.id == int(id))
    print('todo - ', t[0])
    return render_template('form_change.html', data=t[0])


@app.route('/change/edit', methods=["POST"])
def change_edit():
    db_sess = db_session.create_session()
    req = request.form
    id = req.get('id')
    t = db_sess.query(Todo).filter(Todo.id == int(id))
    t[0].text = req.get('text')
    t[0].type = req.get('type')
    db_sess.commit()
    return redirect('/')


@app.route('/remove/<id>', methods=["GET", "POST"])
def remove(id):
    db_sess = db_session.create_session()
    db_sess.query(Todo).filter(Todo.id == int(id)).delete()
    db_sess.commit()
    return redirect('/')


@app.route('/sort_fast')
def sort_fast():
    db_sess = db_session.create_session()
    t = db_sess.query(Todo).all()
    t.sort(key=lambda x: x.type)
    return render_template('table.html', data=t)


@app.route('/sort_slow')
def sort_slow():
    db_sess = db_session.create_session()
    t = db_sess.query(Todo).all()
    t.sort(key=lambda x: x.type, reverse=True)
    return render_template('table.html', data=t)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/sort_date_new')
def sort_date_new():
    db_sess = db_session.create_session()
    t = db_sess.query(Todo).all()
    t.sort(key=lambda x: x.id, reverse=True)
    return render_template('table.html', data=t)


@app.route('/search', methods=["GET", "POST"])
def search():
    req = request.form
    db_sess = db_session.create_session()
    t = db_sess.query(Todo).filter(Todo.text.like(f'%{req.get("search")}%'))
    return render_template('table.html', data=t)


@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        req = request.form
        t = Todo()
        t.text = req.get('text')
        if req.get('type') == 'slow':
            t.type = "slow"
        else:
            t.type = "fast"
        db_sess = db_session.create_session()
        db_sess.add(t)
        db_sess.commit()
        return redirect('/')
    return render_template('form.html')


if __name__ == '__main__':
    main()
