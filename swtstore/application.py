# -*-  coding: utf-8 -*-
"""
    __init__.py
"""

import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request, jsonify, render_template, make_response

from classes.database import db
from config import DefaultConfig
from classes import views
#from classes import models
from classes import oauth

__all__ = ['create_app', 'getDBInstance']

DEFAULT_APP_NAME = __name__

DEFAULT_MODULES = (
    (views.frontend, ''),
    (views.api, '/api'),
    (views.user, '/users'),
    (views.context, '/contexts'),
    (views.sweet, '/sweets'),
    (views.app, '/apps'),
    (views.Oauth, '/oauth')
)


def create_app(config=None, app_name=None, modules=None):

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(app_name)

    configure_app(app, config)

    configure_logging(app)
    configure_errorhandlers(app)
    configure_extensions(app)
    #configure_beforehandlers(app)
    configure_modules(app, modules)

    return app


def configure_app(app, config):

    app.config.from_object(DefaultConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('APP_CONFIG', silent=True)


def configure_modules(app, modules):
    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)


def configure_extensions(app):
    db.init_app(app)
    db.app = app
    oauth.init_app(app)


# return the current db instance
# TODO: is this needed so much?
def getDBInstance():
    return db


def configure_errorhandlers(app):

    if app.testing:
        return

    # TODO: with all these request can we send back the respective HTTP status
    # codes instead of 200?
    @app.errorhandler(404)
    def not_found(error):
        response = make_response()
        response.status_code = 404

        if request.is_xhr:
            response.data = jsonify(error=error)
        else:
            response.data = render_template('errors/404.html')

        return response

    @app.errorhandler(403)
    def forbidden(error):
        response = make_response()
        response.status_code = 403

        if request.is_xhr:
            response.data = jsonify(error=error)
        else:
            response.data = render_template('errors/403.html')

        return response

    @app.errorhandler(401)
    def unauthorized(error):
        response = make_response()
        response.status_code = 401

        if request.is_xhr:
            response.data = jsonify(error=error)
        else:
            response.data = render_template('errors/401.html')

        return response

    @app.errorhandler(400)
    def bad_request(error):
        response = make_response()
        response.status_code = 400

        # Check if we have any custom error messages
        #if g.error:
        #    print 'g.error:'
        #    print g.error
        #    error = g.error

        if request.is_xhr:
            response.data = jsonify(error=error)
        else:
            response.data = render_template('errors/400.html', error=error)

        return response

    @app.errorhandler(500)
    def server_error(error):
        response = make_response()
        response.status_code = 500

        if request.is_xhr:
            response.data = jsonify(error=error)
        else:
            response.data = render_template('errors/500.html')

        return response


def configure_logging(app):

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                                  '[in %(pathname)s:%(lineno)d]')

    # Also error can be sent out via email. So we can also have a SMTPHandler?
    log_file = os.path.join(os.path.dirname(__file__), '..',
                            app.config['LOG_FILE'])

    max_size = 1024 * 1024 * 20  # Max Size for a log file: 20MB
    log_handler = RotatingFileHandler(log_file, maxBytes=max_size,
                                      backupCount=10)

    if 'LOG_LEVEL' in app.config:
        log_level = app.config['LOG_LEVEL'] or 'ERROR'
    else:
        log_level = 'ERROR'

    log_handler.setLevel(log_level)
    log_handler.setFormatter(formatter)

    app.logger.addHandler(log_handler)
