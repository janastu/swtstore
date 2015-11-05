# -*- coding: utf-8 -*-

# classes/sweet.py
# class:: Sweet

from flask import current_app
from datetime import datetime

from sqlalchemy import func

from swtstore.classes.database import db
# custom SQLAlchemy type JSONType
from swtstore.classes.models.types import JSONType
# normalize URLs
from swtstore.classes.utils import urlnorm
from swtstore.classes.utils.httputils import is_url
from swtstore.classes.models import Context, User

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
        """
        Usage: Sweet(who, what, where, how)
                who = <instance of class User>,
                what = <instance of class Context>,
                where = <a valid URL>,
                how = <dict>
        """
        current_app.logger.info('Constructing Sweet..')

        if not isinstance(who, User):
            raise TypeError('`who` should be an instance of User class')
        self.who = who

        if not isinstance(what, Context):
            raise TypeError('`what` should be an instance of Context class')
        self.what = what

        if not is_url(where):
            raise TypeError('`where` is not a valid URL')
        self.where = urlnorm(where)

        if not isinstance(how, dict):
            raise TypeError('`how` attribute should be of type dict')
        self.how = how

    # Update the sweet - only 'how' and 'where' fields can be updated
    def update(self, **kwargs):
        if kwargs.get('how'):
            self.how = kwargs.get('how')
        if kwargs.get('where'):
            self.where = kwargs.get('where')

        self.persist()

    # get Sweets for frontend
    @staticmethod
    def getFrontendSwts(page_num):
        # get <SWTS_PER_PAGE> no. of swts, with an offset of <page_num>
        return Sweet.query.order_by(Sweet.created.desc()).paginate(
            page_num, SWTS_PER_PAGE, False)

    # get all sweets authored by a particular user
    @staticmethod
    def getByCreator(user):
        return Sweet.queryByAll({'who': user})

    # get all sweets by a particular context
    @staticmethod
    def getByContext(context):
        return Sweet.queryByAll({'what': context})

    # get all sweets by a particular URI
    @staticmethod
    def getByURI(uri):
        return Sweet.queryByAll({'where': uri})

    # allow to query all sweets based on "who", "what" and "where" params
    @staticmethod
    def queryByAll(params):
        if params.get('who'):
            params['who'] = User.getByName(params['who'])
        if params.get('what'):
            params['what'] = Context.getByName(params['what'])

        return Sweet.query.filter_by(**params).order_by(Sweet.created.desc()).\
            all()

    # query for count of sweets grouped by user
    @staticmethod
    def queryGroupByUsername():
        return db.session.query(User.username,
                                func.count(Sweet.id)).filter(
                                    Sweet.user_id == User.id).group_by(
                                        User.username).all()

    # create and persist the sweet to the database
    def persist(self):
        current_app.logger.debug('Commiting sweet %s to db', self)
        db.session.add(self)
        db.session.commit()

    # return a dictionary of data members
    def to_dict(self):
        return {
            'id': self.id,
            'who': self.who.to_dict(),
            'what': self.what.to_dict(),
            'where': self.where,
            'how': self.how,
            # 'created': self.created.isoformat()
            'created': self.created.strftime('%a, %d %b %Y, %I:%M %p UTC')
        }

    def __repr__(self):
        return u'{SWTObject: <%s : @%s: #%s : %s>}' % (self.id, self.who,
                                                       self.what, self.where)

    def __str__(self):
        return u'{SWTObject: <%s : @%s: #%s : %s>}' % (self.id, self.who,
                                                       self.what, self.where)
