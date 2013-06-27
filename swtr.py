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
# configuration
DATABASE = 'alipiBlog'
COLLECTION_NAME = 'posts'
DEBUG = True
SECRET_KEY = conf.SECRET_KEY
USERNAME = 'admin'
PASSWORD = 'default'
DB_PORT = 27017
DB_HOST = 'localhost'
URL = "http://localhost:5001"
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Jinja filters
app.jinja_env.filters['len'] = len


def validateSweet(payload):
    for i in payload:
        if len(i['who']) and len(i['what']) and len(i['where']) and len(i['how']):
            pass
        else:
            return False
        return True

@app.before_request
def init_db():
    g.connection = Connection(app.config['DB_HOST'], app.config['DB_PORT'])
    db = g.connection[app.config['DATABASE']]
    g.collection = db[app.config["COLLECTION_NAME"]]


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
    res = g.collection.find().sort('_id',direction=-1)
    entries = make_list(res)
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    data = {}
    data_list = []
    try:
        payload = json.loads(request.form['data'])
    except:
        payload = [{'who': request.form['who'], 'what': request.form['what'],
               'where': request.form['where'], 'how': request.form['how']}]
    valid = validateSweet(payload)
    if not valid:
        response.status_code = 400
        response.data = "Bad or Malformed Request. Please check the validity\
        of your request"
        return response
    print 'swt payload rcvd..'
    print payload
    for i in payload:
        id = g.collection.insert(i)
        data['permalink'] = app.config['URL'] + '/posts/' + str(ObjectId(id))
        data['id'] = str(ObjectId(id))
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
        print session["logged_in"]
        session['key'] = conf.SECRET_KEY
        return render_template('user.html')
    else:
        return render_template('login.html', error=None)

@app.route('/user', methods=['POST', "GET"])
def user():
    if request.method == 'POST':
        response = make_response()
        db = g.connection[app.config['DATABASE']]
        collection = db['sweet_users']
        collection.insert({'user':request.form["user"],"key":request.form["key"]})
        return response
    elif request.method == 'GET':
        db = g.connection[app.config['DATABASE']]
        collection = db['sweet_users']
        users = []
        for user in collection.find():
            users.append(user['user'])
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
                response.status_code = 403
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
    elif request.method == "GET":
        return app.send_static_file("sweet-authenticate.js")


def make_list(res):
    entries = []
    for row in res:
        d = row
        d['id'] = str(row['_id'])
        # d['text'] = row['text']
        # d["title"] = row["title"]
        # d["user"] = row["user"]
        entries.append(d)
    return entries

if __name__ == '__main__':
    app.run(debug=True, port=5001)
