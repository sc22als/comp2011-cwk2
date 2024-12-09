"""
This file initialises app folder to turn it into a python package, to be easily imported.

Also sets up app and database.
"""

from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Section 8 flask admin:
# imports request, session too from flask
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager
from flask_ckeditor import CKEditor

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask(__name__) # app = name of this file
app.config.from_object('config')  # Load the configuration from config.py

#Initialise extensions
db = SQLAlchemy(app)  # Create SQLAlchemy obj with settings from config
migrate = Migrate(app, db)  # Create a Migrate instance
babel = Babel(app, locale_selector=get_locale)
admin = Admin(app, template_mode='bootstrap4')

# Flask_Login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Add CKEditor
ckeditor = CKEditor(app)

# Import routes and models to bind them to the app
from app import views, models, admin