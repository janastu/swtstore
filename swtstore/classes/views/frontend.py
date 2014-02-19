# -*- coding utf-8 -*-
# classes/views/frontend.py


from flask import Module, jsonify, request, render_template

from swtstore.classes.models import Sweet


frontend = Module(__name__)

@frontend.route('/', methods=['GET'])
def index():
    # sweets = Sweet.query.somethingToGetRelevant()
    sweets = Sweet.query.all()
    return render_template('index.html', sweets=sweets)

@frontend.route('/sweets', methods=['POST'])
def saveSweet():
    pass

# Create a new sweet context
@frontend.route('/context/create', methods=['GET', 'POST'])
def createContext():
    pass
