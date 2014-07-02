# -*- coding utf-8 -*-
# classes/views/oauth.py

from flask import Module, jsonify, request, render_template, current_app,\
    make_response, json

from swtstore.classes import oauth
from swtstore.classes.models import Client, AuthorizedClients, User
from swtstore.config import DefaultConfig
from swtstore.classes.utils.httputils import makeCORSHeaders


Oauth = Module(__name__)

config = DefaultConfig()


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


@Oauth.route('/token-expires-in', methods=['GET'])
def token_expires_in():
    response = make_response()
    origin = request.headers.get('Origin', '*')
    response = makeCORSHeaders(response, origin)

    if request.method == 'OPTIONS':
        response.status_code = 200
        return response

    response.data = json.dumps({'expires_in':
                                config.OAUTH2_PROVIDER_TOKEN_EXPIRES_IN})
    return response


@Oauth.route('/errors')
def error():
    return jsonify(error=request.args.get('error'))
