# -*- coding utf-8 -*-
# classes/views/users.py

import requests

from flask import Module, jsonify, request, render_template, session,\
                make_response, url_for, redirect
import json

from swtstore.classes.models.um import User

from swtstore.classes.utils.httputils import make_cross_origin_headers
from swtstore.config import DefaultConfig


config = DefaultConfig()

user = Module(__name__)

@user.route('/login', methods=['POST'])
def login():

    response = make_response()
    response = make_cross_origin_headers(response)

    if 'assertion' not in request.form:
        response.status_code = 400
        return response

    print request.remote_addr
    data = {'assertion': request.form['assertion'], 'audience':
            'http://localhost:5001'}

    resp = requests.post(config.MOZ_PERSONA_VERIFIER, data=data, verify=True)
    print resp.status_code
    print resp.json()

    if resp.ok:
        verified_data = json.loads(resp.content)
        if verified_data['status'] == 'okay':
            user_email = verified_data['email']
            # check if this user exists in our system
            current_user = User.query.filter_by(email=user_email).first()
            # user doesn't exist; create her
            if current_user is None:
                print 'user with email ' + user_email + ' doesn\'t exist;'
                print 'creating new user:' + user_email
                new_user = User('', user_email)
                new_user.persist()
                current_user = new_user

            #session.update({'email': verified_data['email']})
            print 'logging in user with email' + user_email
            session['email'] = current_user.email

            response.status_code = 200
            response.data = {'email': user_email}
            return response

    response.status_code = 500
    return response

@user.route('/logout', methods=['POST'])
def logout():

    response = make_response()
    response = make_cross_origin_headers(response)

    if 'email' in session:
        print 'logging out '
        print session['email']
        session.pop('email')

    response.status_code = 200
    return response

@user.route('/me', methods=['GET', 'POST'])
def profile():

    current_user = User.getCurrentUser()
    if current_user is None:
        return redirect(url_for('frontend.index'))

    if request.method == 'GET':
        return render_template('me.html', user=current_user)

    username = request.form.get('username')
    print username
    current_user.update(username=username)

    return redirect(url_for('profile'))

