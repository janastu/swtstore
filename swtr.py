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
# configuration
DATABASE = 'alipiBlog'
COLLECTION_NAME = 'posts'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
DB_PORT = 27017
DB_HOST = 'localhost'
URL = "http://localhost:5000"
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


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
    escaped_form_data = json.loads(unquote_plus(request.form['data']))
    for i in escaped_form_data:
        id = g.collection.insert({'user':i['user'],'title':i['title'], 'text':i['text'],'top':i['top'],'bottom':i['bottom'],'left':i['left'],'right':i['right']})
        data['permalink'] = app.config['URL']+'/posts/'+str(ObjectId(id))
        data_list.append(data)
    response.data = json.dumps(data_list)
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


@app.route('/posts/<post_id>',methods=['GET'])
def show_specific_entry(post_id):
    try:
        res = g.collection.find({'_id':ObjectId(post_id)});
        if(res.count() > 0):
            entries = make_list(res)
            return render_template('show_posts.html', entries=entries, str=str)
        else:
            abort(404)
    except InvalidId:
        abort(404)


@app.route('/posts/delete/', methods=['POST'])
def delete_post():
    try:
        g.collection.remove({'_id':ObjectId(request.form['post_id'])})
    except:
        abort(500)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

def make_list(res):
    entries = []
    for row in res:
        d = dict()
        d['id'] = str(row['_id'])
        d['text'] = row['text']
        d["title"] = row["title"]
        d["user"] = row["user"]
        entries.append(d)
    return entries

if __name__ == '__main__':
    app.run()
