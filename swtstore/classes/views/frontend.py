# -*- coding utf-8 -*-
# classes/views/frontend.py


from flask import Module, render_template, current_app

from swtstore.classes.models import Sweet


frontend = Module(__name__)


@frontend.route('/', methods=['GET'])
def index():
    sweets = Sweet.getFrontendSwts()
    sweets = [sweet.to_dict() for sweet in sweets]

    current_app.logger.info('swts count: %s', len(sweets))
    return render_template('frontend/index.html', sweets=sweets)


# Create a new sweet context
@frontend.route('/contexts/create', methods=['GET', 'POST'])
def createContext():
    pass
