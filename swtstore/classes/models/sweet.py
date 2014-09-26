# coding utf-8
# classes/sweet.py
# class:: Sweet

from flask import current_app
from datetime import datetime

from swtstore.classes.database import db
# custom SQLAlchemy type JSONType
from swtstore.classes.models.types import JSONType
from swtstore.classes.utils import urlnorm  # normalize URLs
from swtstore.classes.models import Context, User
from swtstore.classes.exceptions import InvalidPayload, ContextDoNotExist


SWTS_PER_PAGE = 100  # Move this to conf file. TODO


class Sweet(db.Model):
    """ customary docstring """

    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    who = db.relationship('User')

    context_id = db.Column(db.Integer, db.ForeignKey('contexts.id'))
    what = db.relationship('Context')

    where = db.Column(db.UnicodeText, nullable=False)

    how = db.Column(JSONType)

    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, who, what, where, how):
        current_app.logger.info('initing sweet..')
        self.who = who
        self.what = what
        self.where = urlnorm(where)
        self.how = how

    def __repr__(self):
        return u'[Sweet Object: <%s : @%s: #%s : %s>]' % (self.id, self.who,
                                                          self.what, self.where)

    def __str__(self):
        return u'[Sweet Object: <%s : @%s: #%s : %s>]' % (self.id, self.who,
                                                          self.what, self.where)

    # Update the sweet - only 'how' and 'where' fields can be updated
    def update(self, **kwargs):
        if kwargs.get('how'):
            self.how = kwargs.get('how')
            self.persist()
        if kwargs.get('where'):
            self.where = kwargs.get('where')
            self.persist()

        return None

    # create multiple sweets from a list of JSON
    @staticmethod
    def createSweets(who, payload):
        # the payload has to be a list; a list of swts
        for each in payload:
            if 'what' not in each and 'where' not in each and 'how' not in\
                    each:

                raise InvalidPayload('Invalid payload %s \n while creating\
                                     mutiple sweets' % (each))
                return None

        # all ok. create swts from the list now
        swts = []
        for each in payload:

            what = Context.getByName(each['what'])

            if what is None:
                raise ContextDoNotExist('Context %s do not exist!' %
                                        (each['what']))

            current_app.logger.debug('SWEET PAYLOAD\n---\n%s\n%s\n%s\n%s\n----',
                                     who, what, each['where'], each['how'])

            new_sweet = Sweet(who, what, each['where'], each['how'])

            new_sweet.persist()
            current_app.logger.debug('New Sweet %s', new_sweet)
            swts.append(new_sweet)

        return swts

    # get Sweets for frontend
    @staticmethod
    def getFrontendSwts(page_num):
        # get <SWTS_PER_PAGE> no. of swts, with an offset of <page_num>
        return Sweet.query.order_by(Sweet.created.desc()).paginate(
            page_num, SWTS_PER_PAGE, False)

    # get all sweets authored by a particular user
    @staticmethod
    def getByCreator(user):
        return Sweet.query.filter_by(who=user).\
            order_by(Sweet.created.desc()).all()

    # allow to query all sweets based on "who", "what" and "where" params
    @staticmethod
    def queryByAll(params):
        if params.get('who'):
            params['who'] = User.getByName(params['who'])
        if params.get('what'):
            params['what'] = Context.getByName(params['what'])

        return Sweet.query.filter_by(**params).all()

    # return a dictionary of data members
    def to_dict(self):

        return {
            'id': self.id,
            'who': self.who.username,
            'user_id': self.user_id,
            'what': self.what.name,
            'context_id': self.context_id,
            'where': self.where,
            'how': self.how,
            #'created': self.created.isoformat()
            'created': self.created.strftime('%a, %d %b %Y, %I:%M %p UTC')
        }

    # create and persist the sweet to the database
    def persist(self):

        current_app.logger.debug('Commiting sweet %s to db', self)
        db.session.add(self)
        db.session.commit()
