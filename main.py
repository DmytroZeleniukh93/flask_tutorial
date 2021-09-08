import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, session, redirect, g, abort, make_response
from FDataBase import FDataBase

DATABASE = '/tmp/fl.db' #######
DEBUG = True
SECRET_KEY = 'urywe7897rweour'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fl.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.get_menu(), posts=dbase.get_posts_anonce())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) > 1 and len(request.form['post']) > 1:
            res = dbase.add_post(request.form['name'], request.form['post'], request.form['url'])
            print('sdf')
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', menu=dbase.get_menu(), title="Добавление статьи")


@app.route('/post/<int:id_post>')
def show_post(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.get_post(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.get_menu(), title=title, post=post)


@app.route("/cookie")
def cookie():
    x = ''
    if request.cookies.get('q'):
        x = request.cookies.get('q')

    res = make_response(f'<h1>Cookie: {x} </h1>')
    res.set_cookie('q', 'yes')
    return res


@app.route('/delcookie')
def del_cookie():
    res = make_response('<h1> Cookie del </h1>')
    res.set_cookie('q', '')
    return res


if __name__ == '__main__':
    app.run(debug=True)
