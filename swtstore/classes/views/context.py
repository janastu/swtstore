# -*- coding utf-8 -*-
# classes/views/context.py

from flask import Module, request, render_template, redirect,\
    url_for, json, current_app, abort

from swtstore.classes.models import Context, User


context = Module(__name__)


@context.route('/register', methods=['GET', 'POST'])
def register():
    current_user = User.getCurrentUser()
    if current_user is None:
        return redirect(url_for('frontend.index'))

    if request.method == 'GET':
        return render_template('context/register.html')

    if request.method == 'POST':
        if not request.form.get('name') or not request.form.get('defn'):
            abort(400)

    current_app.logger.debug('New Context: defn: %s ',
                             request.form.get('defn'))
    json_ld = json.loads(request.form.get('defn'))
    current_app.logger.debug('Resulting json_ld %s', json_ld)

    new_context = Context(
        name=request.form.get('name'),
        definition=json_ld,
        user_id=current_user.id
    )
    current_app.logger.debug('New Context created: %s', new_context)
    new_context.persist()

    return redirect(url_for('user.myContexts'))
