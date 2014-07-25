# -*- coding utf-8 -*-
# classes/views/frontend.py


from flask import Module, render_template, current_app

from swtstore.classes.models import Sweet


frontend = Module(__name__)


@frontend.route('/', methods=['GET'])
@frontend.route('/<int:page>', methods=['GET'])
def index(page=1):
    sweets = Sweet.getFrontendSwts(page)
    formatted_sweets = [sweet.to_dict() for sweet in sweets.items]

#    current_app.logger.info('swts count: %s', len(sweets))
    return render_template('frontend/index.html', sweets=sweets,
                           formatted_sweets=formatted_sweets)


# Create a new sweet context
@frontend.route('/contexts/create', methods=['GET', 'POST'])
def createContext():
    pass
