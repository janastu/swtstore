# -*- coding utf-8 -*-
# classes/views/oauth.py

from flask import Module, jsonify, request, render_template, redirect, url_for
import json

from swtstore.classes import oauth
from swtstore.classes.models.um import User
from swtstore.classes.models import Client


Oauth = Module(__name__)

@Oauth.route('/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    current_user = User.getCurrentUser()
    if current_user is None:
        return render_template('oauth_login.html')

    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.get(client_id)
        print '/authorize: '
        print client
        kwargs['client'] = client
        kwargs['user'] = current_user
        print kwargs
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    print confirm
    return confirm == 'yes'

@Oauth.route('/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    #print request.form
    print 'access token touched..'
    return None

@Oauth.route('/errors')
def error():
    return jsonify(error=request.args.get('error'))
