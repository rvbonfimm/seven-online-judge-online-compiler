#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess
import os
import time
import pexpect
import json

from flask import Flask, render_template, request, url_for
from flaskext.mysql import MySQL
from pexpect import *
from flask_bcrypt import Bcrypt


mysql = MySQL()

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rogerioo4265416'
app.config['MYSQL_DATABASE_DB'] = 'sevenonlinejudge'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/')
@app.route('/index')
def index():

    title = "Seven Online Judge"

    return render_template('index.html', title=title)


@app.route('/main')
def main():

    title = "Pagina principal"

    return render_template('main.html', title=title)


@app.route('/judges')
def judges():

    title = "Pagina de Julgamento"

    return render_template('judge_exercise.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():

    title = "Pagina de Acesso"

    if (request.method == 'POST'):

        username = request.form['loginField']

        password = request.form['passwordField']

        conn = mysql.connect()

        cursor = conn.cursor()

        cursor.execute("SELECT * from users WHERE username = '" + username + "' AND password = '" + password + "'")

        query_result = []

        user_ip = request.environ['REMOTE_ADDR']

        id_user = []

        name = []

        for item in cursor.fetchall():

            id_user = item[0]

            name = item[1]

            query_result.append(id_user)

            query_result.append(name)

        cursor.close()

        if query_result:

            connection = mysql.get_db()

            cursor = connection.cursor()

            query = ("DELETE FROM session WHERE id_user = %s")

            params = (id_user)

            cursor.execute(query, params)

            connection.commit()

            query = ("INSERT INTO session (user_logged, user_ip, id_user) VALUES (%s, %s, %s)")

            params = (name, user_ip, id_user)

            cursor.execute(query, params)

            connection.commit()

            cursor.close()

            message = "Usuario logado com sucesso."

            return render_template('main.html', title=title, message=message)

        else:

            message = "Usuario ou Senha invalidos. Confira os dados digitados e tente novamente!"

            return render_template('index.html', message=message)

    elif (request.method == 'GET'):

        return render_template('index.html', title=title)       


@app.route('/logout', methods=['POST',''])
def logout():

    connection = mysql.get_db()

    cursor = connection.cursor()

    query = ("DELETE FROM session WHERE id_user = %s")

    params = (id_user)

    cursor.execute(query, params)

    connection.commit()

    cursor.close()

    message = "Usuario deslogado com sucesso."

    return render_template('index.html', message=message)


@app.route('/newUser', methods=['GET','POST'])
def newUser():
    
    title = "Pagina de Novo acesso"

    if request.method == 'POST':

        name = request.form['nameField']

        lastname = request.form['lastnameField']

        email = request.form['emailField']

        username = request.form['usernameField']

        password = request.form['passwordField']

        gender = request.form['gender']

        if not ( name and lastname and email and username and password and gender):

            message = "Voce esqueceu de digitar algum dos campos obrigatorios.\n"

            return render_template('index.html', message=message)

        connection = mysql.get_db()

        cursor = connection.cursor()

        query = ("INSERT INTO users(name, lastname, email, username, password, gender) VALUES (%s, %s, %s, %s, %s, %s)")

        params = (name, lastname, email, username, password, gender)

        cursor.execute(query, params)

        connection.commit()

        message = "Novo Usuario cadastrado com sucesso!\n Let's code, dude!\n"

        return render_template('index.html', message=message)

    elif request.method == 'GET':

        return render_template('newUser.html', title=title)         


@app.route('/exercises')
def exercises():

    title = "Pagina de Exercicios"

    return render_template('judge_exercises.html', title=title)


@app.route('/register', methods=['GET','POST'])
def register():

    title = "Pagina de Novo Usuario"

    return render_template('newUser.html', title=title)


@app.route('/julgar')
def judge():

    return render_template('judge.html')


@app.route('/admin/registerExercise', methods=['GET','POST'])
def registerExercise():

    if(request.method == 'POST'):

        connection = mysql.get_db()

        cursor = connection.cursor()

        exercise_number = request.form.get('exercise_number')

        name = request.form.get('name')

        description = request.form.get('description')

        level = request.form.get('level')

        inputt = request.form.get('input')

        output = request.form.get('output')

        query = ("INSERT INTO exercises (exercise_number, name, description, level, input, output) VALUES (%s, %s, %s, %s, %s, %s)")

        params = (exercise_number, name, description, level, inputt, output)

        cursor.execute(query,params)

        connection.commit()

        cursor.close()

        message = "New exercise was successfully inserted at the bank.\n"

        return render_template('index.html', message=message)

    elif(request.method == 'GET'):

        return render_template('create_exercise.html')
    

@app.route('/registerCode', methods=['POST'])
def registerCode():

    title = "Julgamento de Exercicios"

    exercise_number = request.form.get('exercise_number')

    language = request.form.get('language')

    user_code = request.form.get('codearea')

    user_ip = request.environ['REMOTE_ADDR']

    connection = mysql.get_db()

    cursor = connection.cursor()

    query = ("SELECT id FROM exercises WHERE exercise_number = %s")

    params = (exercise_number)

    cursor.execute(query,params)

    aux = cursor.fetchall()[0][0]

    id_exercise = int(aux)

    query = ("SELECT id_user FROM session WHERE user_ip = %s")

    params = (user_ip)

    cursor.execute(query, params)   

    for item in cursor.fetchall():

        id_user = int(item[0])

    query = ("INSERT INTO judges(code, language, id_exercise, id_user) VALUES (%s, %s, %s, %s)")

    params = (user_code, language, id_exercise, id_user)

    cursor.execute(query, params)

    connection.commit()

    cursor.close()

    # Start to create the user code file to compile
    date_time = (time.strftime("%d%m%Y") + "_" + time.strftime("%H%M%S") )

    base_compiler_dir = (os.getcwd().replace("web", "")) + "compiler/"

    exec_dir = base_compiler_dir + "compiler.py"

    user_file_dir = base_compiler_dir + "tojudge/" + exercise_number + "_" + date_time + "_" + str(id_user) + "." + language

    user_file_dir = str(user_file_dir)

    with open(user_file_dir,"w") as userFile:

        userFile.write(user_code)

        userFile.close()

    cmd = ("python " + str(exec_dir) + " " + str(user_file_dir))

    userCodeOut = pexpect.spawn(cmd, timeout=7)

    index = userCodeOut.expect([pexpect.EOF, pexpect.TIMEOUT])

    if(index == 1 ):

        print("TIMEOUT")

        return "Timeout at web pexpect\n"

    result = str(userCodeOut.before)

    if(result.find('Status 1') != -1):

        result = "Status 1"


    print ("[WEB]" + str(result))

    return render_template('exercise_result.html', title=title, result=result)


if __name__ == '__main__':

    app.run(debug=True)