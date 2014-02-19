# coding utf-8
# classes/context.py
# class:: Context

from datetime import datetime
import json

from swtstore.classes import db
from swtstore.classes.models.types import JSONType
from swtstore.classes.exceptions import AlreadyExistsError


class Context(db.Model):
    """ docstring """

    __tablename__ = 'contexts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    definition = db.Column(JSONType, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=None)

    def __init__(self, name, definition):
        for context in Context.query.all():
            if name == context.name:
                raise AlreadyExistsError('Context with name exists!')
                return

        self.name = name
        self.definition = definition

    def __repr__(self):
        print 'Context Object: <%s>' % self.name

    def __str__(self):
        return 'Context Object: <%s>' % self.name

    def persist(self):
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyExistsError('Error')

    # return a context instance given a name
    @staticmethod
    def getContextByName(name):
        return Context.query.filter_by(name=name).first()

