# -*- coding: utf-8 -*-
# User Management::Group

from datetime import datetime

from swtstore.classes.database import db


class Group(db.Model):
    """
    docstring
    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    creator = db.relationship('User', backref='groups')

    def __init__(self, name, creator):
        self.name = name
        self.creator = creator

    # persist object to database
    def persist(self):
        db.session.add(self)
        db.session.commit()

    # delete from database
    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Group %r>' % self.name
