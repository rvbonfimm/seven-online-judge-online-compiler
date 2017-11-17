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

            return render_template('main_new.html', message=message)

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

        if(password != repassword):

            message = "As senhas nao coincidem."

            return render_template('index.html', message=message)

        hashed_passwd = generate_password_hash(password)

        gender = request.form['gender']

        user = User(name=name, lastname=lastname, email=email, username=username, password=hashed_passwd, gender=gender)

        db.session.add(user)

        db.session.commit()

        message = "Novo Usuario cadastrado com sucesso!\n Let's code!!!\n"

        login_user(user)

        return render_template('presentation.html', message=message)

    elif request.method == 'GET':

        return render_template('new_user.html', title=title)

@app.route('/startuser', methods=['GET','POST'])
@login_required
def startuser():

    if request.method == 'POST':

        user_experience = request.form['programming_experience']

        knownItens = Study.query.all()

        if user_experience == "no":

            checkRegisteredPlan = db.session.query(UserPlan.id_user).filter_by(id_user=current_user.id).first() is not None

            if not(checkRegisteredPlan):

                for item in knownItens:

                    new_plan = UserPlan(id_user=current_user.id, id_study=item.id, status="0")

                    db.session.add(new_plan)

                db.session.commit()

                return render_template('beginning.html', allKnownItens=knownItens)

            else:

                alreadyPlain = "Voce ja possui um Plano de Estudos definido."

                return render_template('main.html', alreadyPlain=alreadyPlain)

        elif user_experience == "yes":

            return render_template('presentation_next.html',allKnownItens=knownItens)

    elif request.method == 'GET':

        return render_template('presentation.html')

@app.route('/startusernext', methods=['GET','POST'])
@login_required
def startusernext():

    if request.method == 'POST':

        knownItens = request.form.getlist('knownItens')

        unknownItens = Study.query.filter(~Study.name.in_(knownItens))

        userLevel = request.form['userlevel']

        checkRegisteredPlan = db.session.query(UserPlan.id_user).filter_by(id_user=current_user.id).first() is not None

        if not(checkRegisteredPlan):

            for item in unknownItens:

                new_plan = UserPlan(id_user=current_user.id, id_study=item.id, status="0")

                db.session.add(new_plan)

            db.session.commit()

            message= "Plano criado com sucesso."

            return render_template('beginning.html', specificKnownItens=knownItens, specificUnknownItens=unknownItens, registeredPlain=message)

        else:

            message = "Voce ja possui um Plano de Estudos definido."

            return render_template('main.html', alreadyPlain=message)

    elif request.method == 'GET':

        return render_template('presentation_next.html')

@app.route('/studies', methods=['GET','POST'])
@login_required
def studies():

    if request.method == 'GET':

        itensToDo = 0
        itensDone = 0
        itensToStudy = []
        itensStudied = []

        planInfo = UserPlan.query.filter_by(id_user=current_user.id)

        for item in planInfo:

            study = Study.query.filter_by(id=item.id_study).first()

            if(item.status == 0):

                itensToDo += 1

                itensToStudy.append(study.name)

            elif(item.status == 1):

                itensDone +=1

                itensStudied.append(study.name)

        return render_template('studies.html', itensToStudy=itensToStudy, itensStudied=itensStudied, itensToDo=itensToDo, itensDone=itensDone)

@app.route('/studydashboard', methods=['GET', 'POST'])
@login_required
def studydashboard():

    return render_template('study_dashboard.html')

@app.route('/statistics', methods=['GET', 'POST'])
@login_required
def statistics():

    return render_template('statistics.html')