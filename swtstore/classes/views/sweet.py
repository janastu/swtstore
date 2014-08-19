# -*- coding utf-8 -*-
# classes/views/sweet.py


from flask import Module, render_template, abort

from swtstore.classes.models import Sweet


sweet = Module(__name__)


@sweet.route('/<int:id>', methods=['GET'])
def showSweet(id):
    #current_user = User.getCurrentUser()
    #if current_user is None:
    #    return redirect(url_for('index'))

    #user = current_user.to_dict()
    print "recvd sweet id: %s" % (id)
    sweet = Sweet.query.get(id)
    if sweet:
        print "sweet found %s" % (sweet)
        return render_template('sweet/specific.html', sweet=sweet.to_dict())
    else:
        abort(404)
