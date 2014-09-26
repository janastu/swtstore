# -*- coding utf-8 -*-
# classes/models/client.py
# class:: Client

from datetime import datetime, timedelta
from flask import current_app

from swtstore.classes.database import db
from swtstore.classes.models import User
from swtstore.classes import oauth


class Client(db.Model):
    """
    The third-party application registering with the platform
    """

    __tablename__ = 'clients'

    id = db.Column(db.String(40), primary_key=True)

    client_secret = db.Column(db.String(55), nullable=False)

    name = db.Column(db.String(60), nullable=False)

    description = db.Column(db.String(400))

    # creator of the client application
    user_id = db.Column(db.ForeignKey('users.id'))
    creator = db.relationship('User')

    _is_private = db.Column(db.Boolean)

    _host_url = db.Column(db.String(255))

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_id(self):
        return self.id

    @property
    def client_type(self):
        if self._is_private:
            return 'private'
        return 'public'

    @property
    def host_url(self):
        return self._host_url

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

    def __repr__(self):
        return '<Client: %s :: ID: %s>' % (self.name, self.id)

    def __str__(self):
        return '<Client: %s :: ID: %s>' % (self.name, self.id)

    # create and persist the client to the database
    def persist(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getClientsByCreator(user_id):
        clients = Client.query.filter_by(user_id=user_id)
        return [each for each in clients]


class Grant(db.Model):
    """
    A grant token is created in the authorization flow, and will be
    destroyed when the authorization finished. In this case, it would be better
    to store the data in a cache, which would benefit a better performance.
    """
    #TODO: this would perform better if its only in the cache. and not in a db.

    __tablename__ = 'grants'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  ondelete='CASCADE'))
    user = db.relationship('User')

    client_id = db.Column(db.String(40), db.ForeignKey('clients.id'),
                          nullable=False)
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Token(db.Model):
    """
    The final token to be used by a client
    """

    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.String(40), db.ForeignKey('clients.id'),
                          nullable=False)
    client = db.relationship('Client')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []



#TODO: find out how to better structure the following code

# OAuthLib decorators used by OAuthLib in the OAuth flow
@oauth.clientgetter
def loadClient(client_id):
    current_app.logger.debug('@oauth.clientgetter')
    #return Client.query.filter_by(id=client_id).first()
    return Client.query.get(client_id)


@oauth.grantgetter
def loadGrant(client_id, code):
    current_app.logger.debug('@oauth.grantgetter')
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def saveGrant(client_id, code, request, *args, **kwargs):
    current_app.logger.debug('@oauth.grantsetter')
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=User.getCurrentUser(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def loadToken(access_token=None, refresh_token=None):
    current_app.logger.debug('@oauth.tokengetter')
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def saveToken(token, request, *args, **kwargs):
    current_app.logger.debug('@oauth.tokensetter')

    toks = Token.query.filter_by(client_id=request.client.id,
                                 user_id=request.user.id)
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.id,
        user=request.user
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@oauth.usergetter
def getUser():
    return User.getCurrentUser()


# Authorized Clients
class AuthorizedClients(db.Model):
    """
     The clients authorized by users
    """

    __tablename__ = 'authorized_clients'

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.String(40), db.ForeignKey('clients.id'),
                          nullable=False)
    client = db.relationship('Client')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def persist(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def revoke(**kwargs):
        user = kwargs.get('user')
        client = kwargs.get('client')
        authorization = AuthorizedClients.query.filter_by(user_id=user.id,
                                          client_id=client.client_id).first()
        current_app.logger.debug('authorization to be revoked-- %s',
                                 authorization)
        db.session.delete(authorization)
        db.session.commit()

    @staticmethod
    def getByUser(user):
        authorized_clients = [row.client for row in
                AuthorizedClients.query.filter_by(user_id=user.id).all()]

        current_app.logger.debug('authorized clients %s', authorized_clients)

        return authorized_clients
