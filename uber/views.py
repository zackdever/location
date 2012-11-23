from bson.objectid import ObjectId
from functools import wraps

import bcrypt
from pymongo.errors import OperationFailure, DuplicateKeyError
from flask import (request, jsonify, url_for, Response, render_template,
    session, escape, redirect, flash)
from flask.ext.login import (logout_user, login_user, login_required, UserMixin,
    current_user)

from uber import app
from uber.models import Location

class User(UserMixin):
    def __init__(self, username, id):
        self.username = username
        self.id = id

    def is_active(self):
        return True

@app.login_manager.user_loader
def load_user(userid):
    user = app.db.users.find_one(ObjectId(userid))
    return User(user['username'], user['_id']) if user else None

def check_content_type(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'POST' or request.method == 'PUT':
            ctype = request.headers['Content-Type']
            if ctype != 'application/json':
                return bad_request("Expected 'application/json', got '%s'" % ctype)
        return f(*args, **kwargs)
    return decorated
@app.route('/pandas')
@login_required
def pandas(): return 'pandas'

@app.route('/')
def index():
    if current_user.is_authenticated():
        pass
    return render_template('index.html')

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
                login_user(User(user))
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash('That username and/or password is incorrect.', 'error')

    return render_template('login.html')

@app.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/locations/', methods = ['GET', 'POST'])
@check_content_type
def locations():
    if request.method == 'POST':
        location = Location.parse_json(request.json, has_id=False)
        if not location: return bad_request()

        try:
            app.db.locations.insert(location, safe=True)
            location = Location.flatten(location)

            resp = jsonify(location)
            resp.status_code = 201
            resp.headers['Location'] = url_for('locations') + location['id']
            return resp
        except OperationFailure as e:
            return server_error(str(e))

    # GET - show all
    return jsonify({
        'locations' : [Location.flatten(loc) for loc in app.db.locations.find()]
    })

@app.route('/api/locations/<id>', methods = ['GET', 'PUT', 'DELETE'])
@check_content_type
def location(id):
    if not ObjectId.is_valid(id):
        return bad_request("'id' is either missing or is of the wrong type")

    # ok, the id's format is valid, but does it exist?
    oid = ObjectId(id)
    location = app.db.locations.find_one(oid)
    if not location: return not_found()

    if request.method == 'PUT':
        updated = Location.parse_json(request.json, has_id=True)
        if not updated or updated['_id'] != oid: return bad_request()

        try:
            app.db.locations.save(updated, safe=True)
            return jsonify(Location.flatten(updated))
        except OperationFailure as e:
            return server_error(str(e))
    elif request.method == 'DELETE':
        try:
            app.db.locations.remove({ '_id' : oid }, safe=True)
            return Response(status=204, content_type='application/json')
        except OperationFailure as e:
            return server_error(str(e))

    # GET - show location with id
    return jsonify(Location.flatten(location))

### Error handlers ####################
# TODO only return json error if on api route, which should be set in settings
@app.errorhandler(400)
def bad_request(message=None):
    message = message if message != None else request.url
    resp = jsonify({
        'error': {
            'code': 400,
            'message': 'Bad Request: %s' % message,
        }
    })

    resp.status_code = 400
    return resp

@app.errorhandler(404)
def not_found(message=None):
    message = message if message != None else request.url
    resp = jsonify({
        'error': {
            'code': 404,
            'message': 'Not Found: %s' % message,
        }
    })

    resp.status_code = 404
    return resp

@app.errorhandler(500)
def server_error(message=None):
    message = message if message != None else "It's me, not you."
    resp = jsonify({
        'error': {
            'code': 500,
            'message':  message,
        }
    })

    resp.status_code = 404
    return resp
