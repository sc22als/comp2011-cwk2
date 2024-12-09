WTF_CSRF_ENABLED = True
SECRET_KEY = 'a-very-secret-secret'

import os  # Import the os module to interact with the operating system

# Get the absolute path of the current directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the database URI to use SQLite and set the database file name
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# Enable or disable the modification tracking feature of SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = True
