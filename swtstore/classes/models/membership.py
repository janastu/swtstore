# -*- coding utf-8 -*-
# User Management::Membership

from datetime import datetime

from swtstore.classes.database import db


class Membership(db.Model):
    """ docstring """

    __tablename__ = 'memberships'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    gid = db.Column(db.Integer, db.ForeignKey('groups.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='memberships')
    group = db.relationship('Group', backref='memberships')

    def __init__(self, user, group):
        self.user = user
        self.group = group

    # persist in the database
    def persist(self):
        db.session.add(self)
        db.session.commit()

    # delete from a database
    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return'<Membership %d>' % self.uid
