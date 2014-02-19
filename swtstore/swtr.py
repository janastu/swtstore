# -*- coding: utf-8 -*-
"""
    swtr
    ~~~~~~

    http://swtr.us

    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
from pymongo import Connection
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, make_response, jsonify
from urllib import unquote_plus
import json
import conf
import requests

# TODO:
#    restify
#    APIs as follows:
#        GET /sweets/q -> query sweets
#                         args: who, where, what, how
#        GET /sweets/<id> -> get specific sweet
#        POST /sweets -> post sweets (one or a batch of)
#        OPTIONS /sweets - > CORS policy .. understand it better
#   classes!
#   sqlAlchemy
#   Postgres
#   Persona, Auth in API endpoints

# TODO: move this in a config file
# configuration

DATABASE = 'sweets_production'
COLLECTION_NAME = 'posts'
DEBUG = True
SECRET_KEY = conf.SECRET_KEY
USERNAME = 'admin'
PASSWORD = 'default'
DB_PORT = 27017
DB_HOST = 'localhost'
URL = 'http://localhost:5001'
MOZ_PERSONA_VERIFIER = 'https://verifier.login.persona.org/verify'
MOZ_PERSONA_AUDIENCE = 'http://localhost:5000'

appURL_map = {'img-anno': 'http://localhost:5000/?where=',
              're-narration': 'http://y.a11y.in/web?foruri=',
              'idh-mowl': 'http://app.swtr.us/?where=',
              'testFromAPI': 'http://app.swtr.us/?where='}

# create our little application :)
# ^ ... It's going to be big now :P
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Jinja filters
app.jinja_env.filters['len'] = len


def validateSweet(payload):
    for i in payload:
        try:
            if len(i['who']) and len(i['what']) and len(i['where']) and\
               len(i['how']) and len(i['created']):
                pass
            else:
                return False
        except KeyError:
            return False
    return True


def getUsers():
    db = g.connection[app.config['DATABASE']]
    coll = db['sweet_users']
    users = []
    for i in coll.find():
        users.append(i['user'])
    return users

def gatherStats(coll):
    stats = {}
    stats['total_sweets'] = coll.count()
    return stats

@app.before_request
def init_db():
    g.connection = Connection(app.config['DB_HOST'], app.config['DB_PORT'])
    db = g.connection[app.config['DATABASE']]
    g.collection = db[app.config["COLLECTION_NAME"]]
    g.stats = gatherStats(g.collection)


@app.teardown_request
def close_db(exception):
    g.connection.disconnect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.route('/')
def show_entries():
    res = g.collection.find().sort('_id',direction=-1).limit(100)
    entries = make_list(res)
    return render_template('show_entries.html', entries=entries,
                           appURL_map=appURL_map, stats=g.stats)


# TODO: understand if we really need the OPTIONS
@app.route('/sweets', methods=['POST', 'OPTIONS'])
@app.route('/add', methods=['POST', 'OPTIONS'])
def addSweets():
    print request.method

    if request.method == 'OPTIONS':
        response = make_response()
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] =\
        'http://localhost:5000'
        response.headers['Access-Control-Max-Age'] = '20days'
        response.headers['Access-Control-Allow-Headers'] = 'Origin,\
                         X-Requested-With, Content-Type, Accept'
        return response

    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    response.headers['Access-Control-Allow-Headers'] = 'Origin,\
                     X-Requested-With, Content-Type, Accept'
    data = {}
    data_list = []

    if 'email' in session:
        print 'identifed user'
        print session['email']
    else:
        print 'unidentified user'

    # TODO: find a better way of handling reqeust sweets
    try:
        payload = json.loads(request.form['data'])
    except:
        try:
            payload = [{'who': request.form['who'], 'what': request.form['what'],
                    'where': request.form['where'], 'how': request.form['how']}]
        except:
            try:
                payload = request.json
            except:
                payload = json.loads(request.data)


    valid = validateSweet(payload)
    if not valid:
        response.status_code = 400
        response.data = "Bad or Malformed Request. Please check the validity\
        of your request"
        return response
    print 'swt payload rcvd..'
    print payload
    for i in payload:
        data = i
        id = g.collection.insert(i)
        data['permalink'] = app.config['URL'] + '/posts/' + str(ObjectId(id))
        data['id'] = str(ObjectId(id))
        del(data['_id'])
        print 'data', data
        data_list.append(data)
    response.data = json.dumps(data_list)
    print 'swt stored..'
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/sweets/q', methods=['GET'])
def searchSweets():
    response = make_response()
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    response.headers['Access-Control-Max-Age'] = '20days'
    response.headers['Access-Control-Allow-Headers'] = 'Origin,\
                      X-Requested-With, Content-Type, Accept'

    args = request.args

    if args is None:
        reponse.status_code = 400
        return response

    #if args['where'] is None:
    #    reponse.status_code = 400
    #    return response

    params = {}

    if args.get('where'):
        params['where'] = args.get('where')
    if args.get('who'):
        params['who'] = args.get('who')
    if args.get('what'):
        params['what'] = args.get('what')
    if args.get('how'):
        params['how'] = args.get('how')


    print params
    res = g.collection.find(params)

    if res.count() < 1:
        response.status_code = 404
        return response

    swt_list = []
    for swt in res:
        _id = swt['_id']
        del(swt['_id'])
        swt['id'] = str(_id)
        swt_list.append(swt)

    response.data = json.dumps(swt_list)
    return response


@app.route('/sweets/<post_id>', methods=['GET'])
@app.route('/query/<post_id>',methods=['GET'])
def return_database_entry(post_id):
    try:
        res = g.collection.find_one({'_id':ObjectId(post_id)})
        if(res):
            res['blog'] = url_for('show_specific_entry', post_id = str(res['_id']))
            del(res['_id'])
            return jsonify(res)
            # entries = make_list(res)
            # return render_template('show_posts.html', entries=res, str=str)
        else:
            abort(404)
    except InvalidId:
        abort(404)



@app.route('/posts/<post_id>',methods=['GET'])
def show_specific_entry(post_id):
    try:
        res = g.collection.find({'_id':ObjectId(post_id)})
        if(res.count() > 0):
            #entries = make_list(res)
            entries = []
            for i in res:
                _id = i['_id']
                del(i['_id'])
                i['id'] = _id
                entries.append(i)
            return render_template('show_posts.html', entries=entries, str=str)
        else:
            abort(404)
    except InvalidId:
        abort(404)


@app.route('/posts/delete/', methods=['POST'])
def delete_post():
    try:
        g.collection.remove({'_id':ObjectId(request.form['post_id'])})
        return jsonify(status='ok')
    except:
        abort(500)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/serveUser')
def serveUser():
    if "logged_in" in session:
        #print session["logged_in"]
        session['key'] = conf.SECRET_KEY
        return render_template('user.html')
    else:
        return render_template('login.html', error=None)

@app.route('/user/', methods=['POST', 'GET'])
@app.route('/user/<user_id>', methods=['GET'])
def user(user_id='all'):
    if request.method == 'POST':
        response = make_response()
        db = g.connection[app.config['DATABASE']]
        collection = db['sweet_users']

        # check if user already exists
        if request.form['user'] in getUsers():
            #print 'user already exists!'
            flash('User already exists!')
            return redirect(url_for('serveUser'))

        # else insert new user
        collection.insert({'user': request.form['user'],
                           'key': request.form['key']})
        response.status_code = 200
        response.data = 'User added.'
        return response

    elif request.method == 'GET':
        db = g.connection[app.config['DATABASE']]
        collection = db['sweet_users']
        users = []
        if user_id == 'all':
            users = getUsers()
        else:
            user = collection.find_one({'user': user_id})
            if user:
                users.append(user['user'])
            else:
                abort(404)
        return render_template("users.html", users=users)


@app.route('/authenticate', methods=['POST','GET'])
def authenticate():
    if request.method == "POST":
        response = make_response()
        db = g.connection[app.config['DATABASE']]
        collection = db['sweet_users']
        for i in collection.find():
            if i['user'] == request.form['user'] and i['key'] == request.form['hash']:
                response.status_code = 200
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            else:
                pass
        response.status_code = 403
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    elif request.method == "GET":
        return app.send_static_file("sweet-authenticate.js")

@app.route('/auth/login', methods=['POST'])
def authLogin():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '20days'
    response.headers['Access-Control-Allow-Headers'] = 'Origin,\
                      X-Requested-With, Content-Type, Accept'

    if 'assertion' not in request.form:
        response.status_code = 400
        return response

    data = {'assertion': request.form['assertion'], 'audience':
            MOZ_PERSONA_AUDIENCE}
    resp = requests.post(MOZ_PERSONA_VERIFIER, data=data, verify=True)
    print resp.status_code
    print resp.json()

    if resp.ok:
        verified_data = json.loads(resp.content)
        if verified_data['status'] == 'okay':
            #session.update({'email': verified_data['email']})
            session['email'] = verified_data['email']
            response.status_code = 200
            response.data = {'email': verified_data['email']}
            return response

    response.status_code = 500
    return response

@app.route('/auth/logout', methods=['POST'])
def authLogout():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '20days'
    response.headers['Access-Control-Allow-Headers'] = 'Origin,\
                      X-Requested-With, Content-Type, Accept'

    if 'email' in session:
        print 'logging out '
        print session['email']
        session.pop('email')

    response.status_code = 200
    return response

def make_list(res):
    entries = []
    for row in res:
        d = row
        d['id'] = str(row['_id'])
        try:
            if d['who'] in getUsers() or d['author'] in getUsers():
                d['registered'] = True
        except KeyError:
            pass
        entries.append(d)
    return entries

if __name__ == '__main__':
    app.run(debug=True, port=5001)


