# config.py
# This file holds configuration variables for the Flask application
# The SECRET_KEY is used for securely signing session cookies and forms
# SQLALCHEMY_DATABASE_URI defines the location oof the SQLite database file

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///campus_closet.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
