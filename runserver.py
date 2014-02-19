# -*- coding: utf-8 -*-
# Script to run the application server in development mode

import sys, os
from swtstore import create_app, getDBInstance

# Get the path to the base directory of the app
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# append the path to the WSGI env path
sys.path.insert(0, BASE_DIR)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
