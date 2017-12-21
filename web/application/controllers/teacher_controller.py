# encoding=utf8

from application import app, db
from flask import render_template, request, url_for

from flask_login import login_user, login_required
from application.models.tables import *


@app.route('/teacher', methods=['GET', 'POST'])
def teacher():

	if request.method == 'GET':

		return render_template('teacher.html')

	elif request.method == 'POST':

		email = request.form.get('textbox_email')

		print("E-mail inputted: %s\n" % email)

		return render_template('teacher.html', email=email)

@app.route('/teacher_main', methods=['GET'])
def teacher_board():

	return render_template('teacher_board_main.html')