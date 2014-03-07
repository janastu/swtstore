
# -*- coding utf-8 -*-
# classes/views/context.py


from flask import Module, jsonify, request, render_template, redirect, url_for
import json

from swtstore.classes.models import Context
from swtstore.classes.models.um import User


context = Module(__name__)

@context.route('/', methods=['GET'])
# list apps owned by current user
def list():
    current_user = User.getCurrentUser()
    if current_user is None:
        return redirect(url_for('index'))

    her_contexts = Context.getByCreator(current_user.id)
    print 'her_apps'
    print her_contexts

    return render_template('list_contexts.html', contexts=her_contexts,
                           user=current_user.to_dict())


@context.route('/register', methods=['GET', 'POST'])
def register():
    current_user = User.getCurrentUser()
    if current_user is None:
        return redirect(url_for('index'))

    user = current_user.to_dict()

    if request.method == 'GET':
        return render_template('register_context.html', user=user)

    if request.method == 'POST':
      if not request.form.get('name') or not request.form.get('defn'):
          abort(400)

    print request.form.get('defn')
    json_ld = json.loads(request.form.get('defn'))
    print json_ld

    new_context = Context(
        name = request.form.get('name'),
        definition = json_ld,
        user_id = current_user.id
    )
    print new_context
    new_context.persist()

    return redirect(url_for('list'))

