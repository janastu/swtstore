# coding utf-8

import sys, os

BASE_DIR = os.path.join(os.path.dirname(__file__))

sys.path.insert(0, BASE_DIR)

from swtstore import create_app, getDBInstance

app = create_app()

db = getDBInstance()

# Import all modules which represents a SQLAlchemy model
# They have correspondin tables that are needed to be created
from swtstore.classes.models import Sweet, Context, Client
from swtstore.classes.models.um import User, Group, Membership

db.create_all()


