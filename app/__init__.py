# from config import Config
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app_settings = os.environ['APP_SETTINGS']

# `_is_testing` is defined in `tests.conftest.py`.
if hasattr(sys, '_is_testing'):
    # Setup the app to test mode.
    app_settings = 'config.TestingConfig'

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
