# -*- coding: utf-8 -*-

# classes/context.py
# class:: Context

from datetime import datetime

from sqlalchemy.exc import IntegrityError

from swtstore.classes import db
from swtstore.classes.models.types import JSONType
from swtstore.classes.exceptions import AlreadyExistsError
from swtstore.classes.models import User


class Context(db.Model):
    """ docstring """

    __tablename__ = 'contexts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    definition = db.Column(JSONType, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=None)

    user_id = db.Column(db.ForeignKey('users.id'))
    creator = db.relationship('User')

    def __init__(self, name, definition, creator):
        """
        Usage: Context(name, definition, creator)
                name = <str>
                definition = <dict>
                creator = <instance of class User>
        """
        if not isinstance(name, str):
            TypeError('`name` should be of type str')

        for context in Context.query.all():
            if name == context.name:
                raise AlreadyExistsError('Context with name: %s exists!' % name)
        self.name = name

        if not isinstance(definition, dict):
            raise TypeError('`definition` attribute should be of type dict')
        self.definition = definition

        if not isinstance(creator, User):
            raise TypeError('`creator` should be an instance of class User')
        self.creator = creator

    def __repr__(self):
        return 'Context Object: <%s>' % self.name

    def __str__(self):
        return 'Context Object: <%s>' % self.name

    def persist(self):
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError('Context with name: %s exists!' %
                                     self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'definition': self.definition,
            'creator': self.creator.to_dict(),
            'created': self.created.isoformat(),
            'modified': self.modified
        }

    # return a context instance given a name
    @staticmethod
    def getByName(name):
        return Context.query.filter_by(name=name).first()

    @staticmethod
    def getByCreator(user):
        return Context.query.filter_by(creator=user).all()

    @staticmethod
    def getAll():
        return Context.query.all()
