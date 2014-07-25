# -*- coding utf-8 -*-
# classes/views/frontend.py


from flask import Module, render_template, current_app, request

from swtstore.classes.models import Sweet


frontend = Module(__name__)


@frontend.route('/', methods=['GET'])
def index():

    page = 1
    if request.args.get('page'):
        page = int(request.args.get('page'))

    paginated_swts = Sweet.getFrontendSwts(page)
    sweets = [sweet.to_dict() for sweet in paginated_swts.items]

    current_app.logger.info('swts count: %s', len(sweets))

    return render_template('frontend/index.html', sweets=sweets,
                           paginated_swts=paginated_swts)


# Create a new sweet context
@frontend.route('/contexts/create', methods=['GET', 'POST'])
def createContext():
    pass
