import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql://root:rogerioo4265416@localhost/sevenonlinejudge'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = os.urandom(24)

