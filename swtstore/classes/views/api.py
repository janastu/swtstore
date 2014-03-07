from flask import Module, jsonify, request, make_response, abort, g
import json
from sqlalchemy.exc import IntegrityError

from swtstore.classes.models import Context
from swtstore.classes.models import Sweet
from swtstore.classes.exceptions import AlreadyExistsError
from swtstore.classes.utils import urlnorm # normalize URLs
from swtstore.classes.utils.httputils import make_cross_origin_headers


api = Module(__name__)



# Get a specific sweet
@api.route('/sweets/<int:id>', methods=['GET'])
def getSweetById(id):
    try:
        sweet = Sweet.query.get(id)
    except:
        abort(404)

    if sweet is None:
        abort(404)

    print sweet
    return jsonify(sweet.to_dict())


# Post a sweet to the sweet store
@api.route('/sweets', methods=['OPTIONS', 'POST'])
def createSweet():

    response = make_response()

    #TODO: check if response is coming from a registered client
    response = make_cross_origin_headers(response)

    if request.method == 'OPTIONS':
        response.status_code = 200
        return response

    if request.json:
        payload = request.json
    if request.data:
        payload = json.loads(request.data)
    else:
        print 'data not found in payload!'
        g.error= 'data not found in payload!'
        abort(400)

    print 'new sweet payload recvd..'
    print payload

    if 'who' not in payload and 'what' not in payload and 'where' not in\
       payload and 'how' not in payload:

        print 'Invalid Request..'
        abort(400)

    #who = User.getUserByName(payload['who'])

    what = Context.query.filter_by(name=payload['what']).first()

    if what is None:
        print 'Context doesn\'t exist'
        g.error = 'Context doesn\'t exist'
        abort(400) # this context doesn't exist!

    print 'SWEET DATA'
    print '------------'
    print payload['who']
    print what
    print payload['where']
    print payload['how']
    print '-------------'

    new_sweet = Sweet(payload['who'], what, payload['where'], payload['how'])

    print new_sweet
    new_sweet.persist()

    response.status_code = 200
    return response



# The Sweet query API: /sweets/q?who=<>&what=<>&where=<>
# args: who, what, where
@api.route('/sweets/q', methods=['GET'])
def querySweets():

    args = request.args

    # if no arguments are passed, its an invalid request
    if args is None:
        abort(400)

    params = {}
    if args.get('who'):
        params['who'] = args.get('who')
    if args.get('what'):
        what = Context.query.filter_by(name=args.get('what')).first()
        params['what'] = what
    if args.get('where'):
        params['where'] = urlnorm(args.get('where'))

    # if none of the above parameters are present, its an invalid request
    if len(params) == 0:
        abort(400)

    print 'recvd params'
    print params

    response = make_response()

    sweets = Sweet.query.filter_by(**params).all()

    if len(sweets) == 0:
        abort(404)

    swts = [i.to_dict() for i in sweets]

    response.data = json.dumps(swts)
    response.headers['Content-type'] = 'application/json'
    return response


# Get a specific context with its definition; based on name
@api.route('/contexts/<name>', methods=['GET'])
def getContextByName(name):

    context = Context.query.filter_by(name=name).first()
    if context is None:
        abort(404)

    print context
    return jsonify(context.to_dict())

# Get a specific context with its definition; based on id
@api.route('/contexts/<int:id>', methods=['GET'])
def getContextById(id):

    context = Context.query.get(id)
    if context is None:
        abort(404)

    print context
    print context.created
    print context.to_dict()
    print jsonify(context.to_dict()).data
    return jsonify(context.to_dict())


# Create a new Sweet Context
@api.route('/contexts', methods=['POST'])
def createContext():

    response = make_response()

    # try our best to get the data from request object
    if request.json:
        payload = request.json
    elif request.data:
        payload = json.loads(request.data)
    else:
        # if not found send back a 400
        abort(400)

    #TODO: change it to logger component
    print 'new context payload recvd..'
    print payload

    # if data is invalid send back 400
    if 'name' not in payload and 'definition' not in payload:
        abort(400)

    try:
        new_context = Context(payload['name'], payload['definition'])

    except AlreadyExistsError:
        # context with same name exists; send back 400?
        print 'Already Exists Error'
        abort(400)

    print 'new context'
    print new_context
    # all ok. save the new context
    res = new_context.persist()

    response.status_code = 200
    return response

