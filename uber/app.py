from flask import Flask, request, url_for, json
app = Flask(__name__)

@app.route('/')
def index():
    return 'you see a map.\n'

@app.errorhandler(400)
@app.route('/locations/', methods = ['GET', 'POST'])
def locations():
    if request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            return '[POST %s] expected "application/json", but got "%s"\n' \
                % (url_for('locations'), request.headers['Content-Type']), 400
        else:
            # TODO: return result of saving new location
            return 'ECHO: ' + json.dumps(request.json)

    # TODO: return all locations
    return 'favorite locations\n'

@app.errorhandler(404)
@app.route('/locations/<int:id>')
def location(id, methods = ['GET', 'PUT', 'DELETE']):
    # check if the location exists, if it's missing, 404
        #return '[GET %s] cannot find resource' % url_for(location, id), 404
    if request.method == 'PUT':
        pass
        # update location
    elif request.method == 'DELETE':
        pass
        # delete location

    return 'location %d\n' % id

if __name__ == '__main__':
    app.debug = True
    app.run()
