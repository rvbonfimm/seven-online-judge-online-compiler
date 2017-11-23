# encoding=utf8

from application import app, db, lm
from flask import render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from application.models.tables import User, Study, UserPlan


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/login', methods=['GET', 'POST'])
def login():

    title = "Pagina de Acesso"

    if (request.method == 'POST'):

        username = request.form['loginField']

        password = request.form['passwordField']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            message = "Logado com sucesso."

            return render_template('main.html', message=message)

        else:

            message = "Usuario ou Senha invalidos. Confira os dados digitados e tente novamente!"

            return render_template('login.html', message=message)

    elif (request.method == 'GET'):

        return render_template('login.html', title=title)       

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():

    logout_user()

    message = "Usuario deslogado com sucesso."

    return render_template('login.html',message=message)

@app.route('/registeruser', methods=['GET','POST'])
def registeruser():
    
    title = "Pagina de Novo acesso"

    if request.method == 'POST':

        name = request.form['nameField']

        lastname = request.form['lastnameField']

        email = request.form['emailField']

        username = request.form['usernameField']

        password = request.form['passwordField']

        repassword = request.form['repasswordField']

        gender = request.form['gender']

        if(password != repassword):

            message = "As senhas digitadas não coincidem. Favor redigitá-las!"

            return render_template('new_user.html', message=message, name=name, lastname=lastname, email=email, username=username, gender=gender)

        hashed_passwd = generate_password_hash(password)

        user = User(name=name, lastname=lastname, email=email, username=username, password=hashed_passwd, gender=gender)

        db.session.add(user)

        db.session.commit()

        message = "Novo Usuario cadastrado com sucesso!\n Let's code!!!\n"

        login_user(user)

        return render_template('presentation.html', message=message)

    elif request.method == 'GET':

        return render_template('new_user.html', title=title)

@app.route('/statistics', methods=['GET', 'POST'])
@login_required
def statistics():

    return render_template('statistics.html')