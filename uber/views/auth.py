import bcrypt
from bson.objectid import ObjectId
from flask import request, url_for, render_template, escape, redirect, flash
from flask.ext.login import logout_user, login_user, UserMixin
from pymongo.errors import DuplicateKeyError

from uber import app

app.login_manager.login_view = 'login'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            flash('Please provide both your username and password', 'error')
        else:
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            user = app.db.users.find_one({ 'username': username })

            if user and bcrypt.hashpw(password, user['password']) == user['password']:
                login_user(User(username, str(user['_id'])))
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash('That username and/or password is incorrect.', 'error')

    next = request.args.get('next') or ''
    return render_template('login.html', next=next)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            flash('Please provide both a username and password.', 'error')
        else:
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            try:
                userid = app.db.users.insert({'username':username, 'password': hashed},
                    safe=True)
                login_user(User(username, str(userid)))
                flash('You are now logged in!', 'info')
                return redirect(url_for('index'))
            except DuplicateKeyError:
                flash("Sorry, but '%s' is already taken." % escape(username),
                    'error')

    return render_template('register.html')

@app.login_manager.user_loader
def load_user(userid):
    user = app.db.users.find_one(ObjectId(userid))
    return User(user['username'], user['_id']) if user else None

class User(UserMixin):
    def __init__(self, username, id):
        self.username = username
        self.id = id

    def is_active(self):
        return True
