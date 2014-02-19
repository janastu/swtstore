# coding utf-8

import sys, os

BASE_DIR = os.path.join(os.path.dirname(__file__))

sys.path.insert(0, BASE_DIR)

from swtstore import create_app, getDBInstance
from swtstore.classes.models import Sweet, Context
from swtstore.classes.models.um import User, Group, Membership, setup_app



app = create_app()

setup_app(app)

db = getDBInstance()

db.create_all()
