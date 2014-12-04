from flask import Module, jsonify, request, make_response
from flask import abort, g, json, current_app

from swtstore.classes.models import Context, Sweet
from swtstore.classes.exceptions import AlreadyExistsError, InvalidPayload,\
    ContextDoNotExist
from swtstore.classes.utils import urlnorm  # normalize URLs
from swtstore.classes.utils.httputils import makeCORSHeaders
from swtstore.classes import oauth


api = Module(__name__)


# Get a specific sweet
# Update a specific sweet
@api.route('/sweets/<int:id>', methods=['GET', 'PUT'])
def getSweetById(id):

    # Get a specific sweet
    if request.method == 'GET':
        sweet = Sweet.query.get(id)

        if sweet is None:
            abort(404)

        current_app.logger.debug('getSweetById: %s', sweet)
        return jsonify(sweet.to_dict())

    # Update a specific sweet
    elif request.method == 'PUT':
        payload = request.json
        if payload is None:
            abort(400)

        current_app.logger.debug('Update Sweet: recvd payload: %s', payload)

        sweet = Sweet.query.get(id)

        if sweet is None:
            abort(404)

        current_app.logger.debug('Updating sweet %s with new how: %s ',
                                 sweet.id, payload)

        sweet.update(how=payload)

        return jsonify(sweet.to_dict())


# Post a sweet to the sweet store
@api.route('/sweets', methods=['OPTIONS', 'POST'])
@oauth.require_oauth('email', 'sweet')
def createSweet():

    response = make_response()

    client = request.oauth.client

    #TODO: make a decorator of CORS request
    response = makeCORSHeaders(response, client.host_url)

    if request.method == 'OPTIONS':
        response.status_code = 200
        return response

    payload = request.json or request.data
    if not payload:
        current_app.logger.error('data not found in payload!')
        g.error = 'data not found in payload!'
        abort(400)

    current_app.logger.debug('new sweet payload recvd.. %s', payload)
    if type(payload) is str:
        payload = json.loads(payload)

    current_app.logger.debug('type of payload %s', type(payload))
    # Get the authenticated user from the oauth request object.
    # Older swtr clients sending `who` in string will be ignored.
    who = request.oauth.user

    try:
        swts = Sweet.createSweets(who, payload)
    except (InvalidPayload, ContextDoNotExist) as e:
        current_app.logger.error('Error creating sweets. Error: %s', e)
        current_app.logger.error('Error %s', who)
        abort(400)

    response.status_code = 200
    response.headers['Content-type'] = 'application/json'
    response.data = json.dumps([i.to_dict() for i in swts])
    return response


# The Sweet query API: /sweets/q?who=<>&what=<>&where=<>
# args: who, what, where
@api.route('/sweets/q', methods=['GET', 'OPTIONS'])
#@oauth.require_oauth('sweet')
def querySweets():

    response = make_response()
    origin = request.headers.get('Origin', '*')
    response = makeCORSHeaders(response, origin)

    if request.method == 'OPTIONS':
        response.status_code = 200
        return response

    args = request.args

    # if no arguments are passed, its an invalid request
    if args is None:
        abort(400)

    params = {}
    if args.get('who'):
        params['who'] = args.get('who')
    if args.get('what'):
        params['what'] = args.get('what')
    if args.get('where'):
        params['where'] = urlnorm(args.get('where'))

    # if none of the above parameters are present, its an invalid request
    if len(params) == 0:
        abort(400)

    current_app.logger.debug('recvd params: %s', params)

    sweets = Sweet.queryByAll(params)

    if len(sweets) == 0:
        current_app.logger.info('No sweets found to satisfy query..')
        #abort(404)
        response.data = json.dumps([])

    swts = [i.to_dict() for i in sweets]

    response.data = json.dumps(swts)
    response.headers['Content-type'] = 'application/json'
    return response


# Get a specific context with its definition; based on name
@api.route('/contexts/<name>', methods=['GET'])
def getContextByName(name):

    context = Context.getByName(name)
    if context is None:
        abort(404)

    current_app.logger.debug('getContextByName : %s', context)
    return jsonify(context.to_dict())


# Get a specific context with its definition; based on id
@api.route('/contexts/<int:id>', methods=['GET'])
def getContextById(id):

    context = Context.query.get(id)
    if context is None:
        abort(404)

    current_app.logger.debug('getContextById response: %s',
                             jsonify(context.to_dict()).data)

    return jsonify(context.to_dict())


# Create a new Sweet Context
@oauth.require_oauth('email', 'context')
@api.route('/contexts', methods=['GET', 'POST'])
def createContext():

    if request.method == 'POST':
        response = make_response()

        # try our best to get the data from request object
        if request.json:
            payload = request.json
        elif request.data:
            payload = json.loads(request.data)
        else:
        # if not found send back a 400
            abort(400)

        current_app.logger.debug('new context payload recvd.. %s', payload)

        # if data is invalid send back 400
        if 'name' not in payload and 'definition' not in payload:
            abort(400)

        try:
            new_context = Context(payload['name'], payload['definition'])

        except AlreadyExistsError:
        # context with same name exists; send back 400?
            current_app.logger.info('Context Already Exists Error')
            abort(400)

        current_app.logger.debug('new context created: %s', new_context)

        # all ok. save the new context
        new_context.persist()

        response.status_code = 200
        return response

    else:
        # Get all contexts saved in the store.
        contexts = Context.getAll()
        response = make_response()
        origin = request.headers.get('Origin', '*')
        response = makeCORSHeaders(response, origin)
        if len(contexts) > 0:
            response.data = json.dumps(contexts)
        else:
            response.status_code = 204  # The server successfully processed the
                                        # request, but is not returning any
                                        # content.
            response.data = json.dumps([{'reason': 'No context found.'}])
        return response


# Send back logged in user data
@api.route('/users/me', methods=['GET', 'OPTIONS'])
@oauth.require_oauth('email')
def getCurrentUser():
    response = make_response()
    response = makeCORSHeaders(response, request.oauth.client.host_url)
    response.status_code = 200

    if request.method == 'OPTIONS':
        return response

    response.headers['Content-type'] = 'application/json'
    # We have the user object along with the oauth request. Just return it back
    response.data = json.dumps(request.oauth.user.to_dict())
    return response
