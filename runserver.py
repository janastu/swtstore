# -*- coding: utf-8 -*-
# swtstore->runserver.py

# Script to run the application server in development mode

import sys
import os

# Get the path to the base directory of the app
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# append the path to the WSGI env path
sys.path.insert(0, BASE_DIR)

# Import and create the app
from swtstore import create_app

app = create_app()

# Run the server if this script is directly executed
# Presumably, this is development mode
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
