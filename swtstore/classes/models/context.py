# coding utf-8
# classes/context.py
# class:: Context

from datetime import datetime
import json

from sqlalchemy.exc import IntegrityError

from swtstore.classes import db
from swtstore.classes.models.types import JSONType
from swtstore.classes.exceptions import AlreadyExistsError


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

    def __init__(self, name, definition, user_id):
        for context in Context.query.all():
            if name == context.name:
                raise AlreadyExistsError('Context with name exists!')
                return

        self.name = name
        self.definition = definition
        self.user_id = user_id

    def __repr__(self):
        return 'Context Object: <%s>' % self.name

    def __str__(self):
        return 'Context Object: <%s>' % self.name

    def persist(self):
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError('Error')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'definition': json.dumps(self.definition),
            'created': self.created.isoformat(),
            'modified': self.modified
        }

    # return a context instance given a name
    @staticmethod
    def getByName(name):
        return Context.query.filter_by(name=name).first()

    @staticmethod
    def getByCreator(id):
        return [each.to_dict() for each in Context.query.filter_by(user_id=id)]

    @staticmethod
    def getAll():
        return [each.to_dict() for each in Context.query.all()]
