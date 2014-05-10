# HTTP utilities
from flask import current_app

def makeCORSHeaders(response, host_url):
    current_app.logger.debug('makeCORSHeaders(): client\'s host_url: %s',
                             host_url)
    response.headers['Access-Control-Allow-Origin'] = host_url
    response.headers['Access-Control-Max-Age'] = '3600'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

    current_app.logger.debug('Updated headers %s', response.headers)

    return response

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

"""
def crossdomain(origin=None, methods=None, headers=None, max_age=3600,
                attach_to_all=True, automatic_options=True):

    if methods is not None:
        methods = ', '.join(sorted(i.upper() for i in methods))
    if headers in not None and not isinstance(headers, basestring):
        headers = ', '.join(i.upper() for i in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current

"""
