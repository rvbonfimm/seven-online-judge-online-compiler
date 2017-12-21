import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql://root:mysecuritypass1234@localhost/sevenonlinejudge'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = os.urandom(24)

