import pexpect
import time
import os

from application import app
from flask import Flask, render_template, request, url_for
from pexpect import spawn
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from application.models.tables import User, Exercise, Judge