import os
from datetime import timedelta

class Config:
    # SQLite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'local_secret_key'