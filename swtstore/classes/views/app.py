# -*- coding utf-8 -*-
# classes/views/apps.py

from flask import Module, request, render_template, redirect,\
    url_for, abort

from werkzeug.security import gen_salt

from swtstore.classes.models import Client, User
from swtstore.classes.utils import urlnorm


app = Module(__name__)


@app.route('/register', methods=['GET', 'POST'])
def register():
    current_user = User.getCurrentUser()
    if current_user is None:
        return redirect(url_for('frontend.index'))

    if request.method == 'GET':
        return render_template('app/register.html')

    elif request.method == 'POST':
        req_fields = ['name', 'host_url', 'redirect_uris', 'scopes']
        for field in req_fields:
            if not request.form.get(field):
                abort(404)

        new_app = Client(
            id=gen_salt(40),
            client_secret=gen_salt(50),
            name=request.form.get('name'),
            description=request.form.get('desc'),
            user_id=current_user.id,
            _host_url=request.form.get('host_url'),
            _redirect_uris=urlnorm(request.form.get('redirect_uris')),
            _default_scopes=' '.join(request.form.get('scopes').split(',')),
            _is_private=False
        )
        new_app.persist()

        return redirect(url_for('user.myApps'))
