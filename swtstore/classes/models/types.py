# -*- coding utf-8 -*-
# classes/types.py
# class:: Types
# extend  SQLAlchemy Types

import json

from sqlalchemy import types


class JSONType(types.TypeDecorator):
    """
    An extended type to store JSON as a TEXT in database.
    This class, converts dict to string while storing to database and
    similarly, convert string to dict while loading from database
    """

    impl = types.UnicodeText

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)
