import bcrypt
from flask import (current_app, escape, flash, redirect, render_template,
    request, url_for)
from flask.ext.login import current_user, logout_user, login_user
from pymongo.errors import DuplicateKeyError

from uber.auth import auth
from uber.auth.models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            flash('Please provide both your username and password', 'error')
        else:
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            user = current_app.db.users.find_one({ 'username': username })

            if user and bcrypt.hashpw(password, user['password']) == user['password']:
                login_user(User(username, user['_id']))
                return redirect(request.args.get('next') or url_for('ui.index'))
            else:
                flash('That username and/or password is incorrect.', 'error')

    if current_user.is_authenticated():
        return redirect(url_for('ui.index'))
    next = request.args.get('next')
    action_args = '?next=%s' % next if next is not None else ''
    return render_template('login.html', action_args=action_args)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            flash('Please provide both a username and password.', 'error')
        else:
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            try:
                userid = current_app.db.users.insert({
                            'username': username, 'password': hashed}, safe=True)
                login_user(User(username, userid))
                return redirect(url_for('ui.index'))
            except DuplicateKeyError:
                flash("Sorry, but '%s' is already taken." % escape(username),
                    'error')

    return render_template('register.html')
