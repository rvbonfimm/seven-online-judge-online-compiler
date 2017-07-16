import subprocess
import os
import time
import pexpect

from flask import Flask, render_template, request, url_for
from pexpect import *

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return render_template('main.html')


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')


@app.route('/registerUser', methods=['GET','POST'])
def registerUser():
	
	if request.method == 'POST':

		name = request.form.get('name')
		lastname = request.form.get('lastname')
		email = request.form.get('email')
		username = request.form.get('username')
		password = request.form.get('password')

	return str(codearea)


@app.route('/registerCode', methods=['POST'])
def registerCode():

	USER_CODE = request.form.get('codearea')

	EXERCISE_NUMBER = request.form.get('exercise_number')

	LANGUAGE = request.form.get('language')

	if LANGUAGE == "Python":

		LANGUAGE = "py"

	elif LANGUAGE == "C":

		LANGUAGE = "c"

	DATE_TIME = (time.strftime("%d%m%Y") + "_" + time.strftime("%H%M%S") )

	FILE_DIR = ((os.getcwd().replace("web", "")) + "compiler/")

	COMPILER_DIR = FILE_DIR + "compiler.py"

	USER_FILE = str(FILE_DIR + EXERCISE_NUMBER + "_" + DATE_TIME + "." + LANGUAGE)

	#CMD = ["python", COMPILER_DIR, USER_FILE, '-d']

	CMD = ("python " + str(COMPILER_DIR) + " " + str(USER_FILE) + " -d ")

	print("[App] Code: " + str(USER_CODE))
	print("[App] Exercise: " + str(EXERCISE_NUMBER))
	print("[App] Language: " + str(LANGUAGE))
	print("[App] Date time: " + str(DATE_TIME))
	print("[App] File dir: " + str(FILE_DIR))
	print("[App] Compiler dir: " + str(COMPILER_DIR))
	print("[App] User file: " + str(USER_FILE))
	print("[App] Cmd: " + str(CMD))

	with open(USER_FILE,"w") as userFile:

		userFile.write(USER_CODE)

		userFile.close()

	userCodeOut = pexpect.spawn(CMD, timeout=5)

	checkExpectOut = userCodeOut.expect([pexpect.EOF, pexpect.TIMEOUT])
	
	if(checkExpectOut == 1 ):

		print("TIMEOUT")

	pexpectOut = userCodeOut.before

	print(pexpectOut)	

	#process = subprocess.Popen(CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

	#process.wait()

	#process.communicate()[0]
	
	#if(process.returncode == 1):

	#	print("[App] Not ran")

	#else:

	#	print("[App] Ran")

	return render_template('dashboard_result.html')


if __name__ == '__main__':
	app.run(debug=True)
