# coding utf-8
# classes/sweet.py
# class:: Sweet

from datetime import datetime

from swtstore.classes.database import db
# custom SQLAlchemy type JSONType
from swtstore.classes.models.types import JSONType
from swtstore.classes.utils import urlnorm # normalize URLs

class Sweet(db.Model):
    """ customary docstring """

    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    who = db.relationship('User')

    context_id = db.Column(db.Integer, db.ForeignKey('contexts.id'))
    what = db.relationship('Context')

    where = db.Column(db.String, nullable=False)

    how = db.Column(JSONType)

    created = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, who, what, where, how):
        print 'initing sweet..'
        self.who = who
        self.what = what
        self.where = urlnorm(where)
        self.how = how


    def __repr__(self):
        return '[Sweet Object: <%s : @%s: #%s : %s>]' % (self.id, self.who,
                                                        self.what, self.where)

    def __str__(self):
        return '[Sweet Object: <%s : @%s: #%s : %s>]' % (self.id, self.who,
                                                        self.what, self.where)

    # return a dictionary of data members
    def to_dict(self):
        print self.created
        return {
            'id': self.id,
            'who': self.who,
            'what': self.what.name,
            'context_id': self.context_id,
            'where': self.where,
            'how': self.how,
            'created': self.created.isoformat()
        }


    # create and persist the sweet to the database
    def persist(self):

        db.session.add(self)
        db.session.commit()


