# -*- coding utf-8 -*-
# classes/views/oauth.py

from flask import Module, jsonify, request, render_template, redirect,\
                    url_for, current_app
import requests

from swtstore.classes import oauth
from swtstore.classes.models.um import User
from swtstore.classes.models import Client, AuthorizedClients


Oauth = Module(__name__)


@Oauth.route('/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    current_user = User.getCurrentUser()
    if current_user is None:
        return render_template('oauth/login.html')

    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.get(client_id)
        current_app.logger.debug('In /authorize: client: %s', client)
        kwargs['client'] = client
        kwargs['user'] = current_user
        current_app.logger.debug('kwargs %s', kwargs)

        # See if this client is already authorized by user. If not then return
        # a HTML to allow access.
        authorized_clients = AuthorizedClients.getByUser(current_user)
        if client in authorized_clients:
            return render_template('oauth/authorized.html', **kwargs)
        else:
            return render_template('oauth/authorize.html', **kwargs)


    confirm = request.form.get('confirm', 'no')
    authorized = request.form.get('authorized', 'no')
    current_app.logger.debug('confirm authorize from user: %s', confirm)
    client = Client.query.get(request.form.get('client_id'))

    if authorized == 'yes':
        return True
    else:
        if confirm == 'yes':
            authorization = AuthorizedClients(user=current_user, client=client)
            authorization.persist()
            return True
        else:
            return False


@Oauth.route('/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    #print request.form
    current_app.logger.debug('access token touched..')
    return None

@Oauth.route('/errors')
def error():
    return jsonify(error=request.args.get('error'))

