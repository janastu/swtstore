# -*- coding utf-8 -*-
# classes/views/users.py

import requests

# flask imports
from flask import Module, request, render_template, session,\
    make_response, url_for, redirect, json, current_app, abort

# swtstore imports
from swtstore.classes.models import User, Sweet, Context, Client,\
    AuthorizedClients

from swtstore.config import DefaultConfig


config = DefaultConfig()

user = Module(__name__)


@user.route('/login', methods=['POST'])
def login():

    response = make_response()
    #response = makeCORSHeaders(response)

    if 'assertion' not in request.form:
        response.status_code = 400
        return response

    current_app.logger.debug('remote address of request for user login %s',
                             request.remote_addr)

    data = {'assertion': request.form['assertion'], 'audience':
            config.SWTSTORE_URL}

    resp = requests.post(config.MOZ_PERSONA_VERIFIER, data=data, verify=True)
    current_app.logger.debug('Response code from MOZ_PERSONA_VERIFIER %s',
                             resp.status_code)
    current_app.logger.debug('Response body: %s', resp.json())

    if resp.ok:
        verified_data = json.loads(resp.content)
        if verified_data['status'] == 'okay':
            user_email = verified_data['email']
            # check if this user exists in our system
            current_user = User.query.filter_by(email=user_email).first()
            # user doesn't exist; create her
            if current_user is None:
                current_app.logger.info('user with email %s doesn\'t exist',
                                        user_email)
                current_app.logger.info('creating new user: %s', user_email)

                # get the email_id and use it as a default username
                temp_username = user_email.split('@')[0]
                new_user = User(temp_username, user_email)
                new_user.persist()
                current_user = new_user

            #session.update({'email': verified_data['email']})
            current_app.logger.info('logging in user with email %s',
                                    user_email)
            session['email'] = current_user.email

            response.status_code = 200
            response.data = {'email': user_email}
            return response

    response.status_code = 500
    return response


@user.route('/logout', methods=['POST'])
def logout():

    response = make_response()
    #response = makeCORSHeaders(response)

    if 'email' in session:
        current_app.logger.info('logging out user %s', session['email'])
        session.pop('email')

    response.status_code = 200
    return response


@user.route('/me', methods=['GET', 'POST'])
def profile():

    current_user = User.getCurrentUser()
    if current_user is None:
        return redirect(url_for('frontend.index'))

    if request.method == 'GET':
        return render_template('user/me.html', user=current_user.to_dict())

    # else POST request
    username = request.form.get('username')

    current_app.logger.debug('Updating username of %s to %s',
                             current_user.username, username)

    current_user.update(username=username)

    current_app.logger.debug('url_for(profile): %s', url_for('profile'))
    return redirect(url_for('profile'))


@user.route('/me/sweets', methods=['GET'])
def mySweets():

    user = User.getCurrentUser()
    if user is None:
        return redirect(url_for('frontend.index'))

    swts = Sweet.getByCreator(user)
    swts = [swt.to_dict() for swt in swts]
    return render_template('user/sweets.html', sweets=swts)


@user.route('/me/contexts', methods=['GET'])
def myContexts():

    user = User.getCurrentUser()
    if user is None:
        return redirect(url_for('frontend.index'))

    contexts = Context.getByCreator(user.id)
    return render_template('user/contexts.html', contexts=contexts)


@user.route('/me/apps', methods=['GET'])
def myApps():

    # make a decorator out of this repetative code
    user = User.getCurrentUser()
    if user is None:
        return redirect(url_for('frontend.index'))

    apps = Client.getClientsByCreator(user.id)
    return render_template('user/apps.html', apps=apps)


@user.route('/me/authorized_apps', methods=['GET', 'POST'])
def authorizedApps():

    user = User.getCurrentUser()
    if user is None:
        return redirect(url_for('frontend.index'))

    if request.method == 'GET':
        authorized_clients = AuthorizedClients.getByUser(user)
        return render_template('user/authorized_apps.html',
                               authorized_clients=authorized_clients)

    # else POST request
    client_id = request.form.get('revoke-id', '')
    if client_id:
        client = Client.query.get(client_id)
        current_app.logger.info('user %s revoking access to %s', user, client)
        AuthorizedClients.revoke(user=user, client=client)

    return redirect(url_for('authorizedApps'))


@user.route('/<int:user_id>', methods=['GET'])
def publicProfile(user_id):

    user = User.query.get(user_id)
    if user is None:
        abort(404)

    return render_template('user/profile.html', user=user.to_dict())
