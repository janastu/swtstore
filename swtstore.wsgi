import sys, os

BASE_DIR = os.path.join(os.path.dirname(__file__))

sys.path.insert(0, BASE_DIR)

#import production_settings

from swtstore import create_app

application = create_app()
