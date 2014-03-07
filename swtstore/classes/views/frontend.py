# -*- coding utf-8 -*-
# classes/views/frontend.py


from flask import Module, jsonify, request, render_template, redirect, url_for

from swtstore.classes.models import Sweet
from swtstore.classes.models.um import User


frontend = Module(__name__)

@frontend.route('/', methods=['GET'])
def index():
    # sweets = Sweet.query.somethingToGetRelevant()
    sweets = Sweet.query.all()

    user = User.getCurrentUser()
    if user is not None:
        user = user.to_dict()

    return render_template('index.html', sweets=sweets, user=user)


# Create a new sweet context
@frontend.route('/contexts/create', methods=['GET', 'POST'])
def createContext():
    pass
