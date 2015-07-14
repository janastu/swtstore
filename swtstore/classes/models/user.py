# -*- coding utf-8 -*-
# User Management::User

from datetime import datetime
from flask import session
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from swtstore.classes.database import db


class User(db.Model):
    """ docstring """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    # phone = db.Column(db.String(13), unique=True)
    password = db.Column(db.String(120))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update(self, **kwargs):
        if kwargs.get('username'):
            self.username = kwargs.get('username')
        if kwargs.get('last_active'):
            current_app.logger.debug('Updated last_active timestamp %s for %s',
                                     kwargs.get('last_active'), self)
            self.last_active = kwargs.get('last_active')

        self.persist()

    # persist current object in the database
    def persist(self):
        db.session.add(self)
        db.session.commit()

    # delete from database
    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getCurrentUser():
        if 'email' in session:
            user = User.query.filter_by(email=session['email']).first()
            user.update(last_active=datetime.utcnow())
            return user
        elif 'phone' in session:
            user = User.query.filter_by(email=session['phone']).first()
            user.update(last_active=datetime.utcnow())
            return user

        return None

    @staticmethod
    def getByName(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def getByPhone(phone):
        return User.query.filter_by(phone=phone).first()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            #'created': self.created.isoformat(),
            'created': self.created.strftime('%a, %d %b %Y, %I:%M %p UTC'),
            #'last_active': self.last_active.isoformat()
            'last_active': self.last_active.strftime('%a, %d %b %Y, %I:%M %p UTC')
        }

    def __repr__(self):
        return '<User:: %r %r>' % (self.username, self.email)
