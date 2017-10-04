import pexpect
import time
import os

from application import app, db
from flask import render_template, request, url_for
from pexpect import spawn
from flask_login import login_user, login_required, current_user
from application.models.tables import Exercise, Judge, User, Attempt


@app.route('/test')
@login_required
def test():

    title = "Lista de Exercicios"

    exercises = Exercise.query.all()

    return render_template('list_exercises.html', title=title, exercises_list=exercises)

@app.route('/test2')
@login_required
def test2():

    return render_template('modal_exercises.html')


@app.route('/listexercises')
@login_required
def listexercises():

    title = "Lista de Exercicios"

    exercises = Exercise.query.all()

    return render_template('preview_exercises.html', title=title, exercises_list=exercises)


@app.route('/judges/<int:exercise>', methods=['GET', 'POST'])
@app.route('/judges/', defaults={"exercise": None}, methods=['GET', 'POST'])
@login_required
def judges(exercise):

    title = "Pagina de Julgamento"

    exercises = Exercise.query.all()

    return render_template('judge_exercises.html', title=title, exercises_list=exercises, exercise=exercise)


@app.route('/registercode', methods=['GET', 'POST'])
@login_required
def registercode():

    status = {'Status 1':'Erro de sintaxe','Status 2':'Resposta incorreta','Status 3':'Tempo limite excedido','Status 4':'Erro de apresentacao','Status 5':'Codigo submetido com sucesso'}

    title = "Julgamento de Exercicios"

    exercise_number = request.form.get('exercise_number')

    user_language = request.form.get('language')

    user_code = request.form.get('codearea')

    user_id = current_user.id

    exercise = Exercise.query.filter_by(exercise_number=exercise_number).first()

    id_exercise = exercise.id

    judge = Judge(code=user_code, language=user_language, id_exercise=id_exercise, id_user=user_id)

    #alreadyTried = Attempt.query.filter_by(id_user=user_id).first()

    #if(alreadyTries):

    #elif():

    #else:

    db.session.add(judge)

    db.session.commit()

    # Start to create the user code file to compile
    date_time = (time.strftime("%d%m%Y") + "_" + time.strftime("%H%M%S") )

    base_compiler_dir = (os.getcwd().replace("web", "")) + "compiler/"

    exec_dir = base_compiler_dir + "compiler.py"

    user_file_dir = base_compiler_dir + "tojudge/" + exercise_number + "_" + date_time + "_" + str(user_id) + "." + user_language

    user_file_dir = str(user_file_dir)

    with open(user_file_dir,"w") as userFile:

        userFile.write(user_code)

        userFile.close()

    cmd = ("python " + str(exec_dir) + " " + str(user_file_dir))

    userCodeOut = pexpect.spawn(cmd, timeout=7)

    index = userCodeOut.expect([pexpect.EOF, pexpect.TIMEOUT])

    if(index == 1 ):

        return "[WEB] Timeout exceeded.\n"

    result = userCodeOut.before

    if(result.find('Status 1') != -1):

        result = "Status 1"

    clearResult = str(result).strip()

    if status.has_key(clearResult):

        value = status[clearResult]

    attempt = Attempt(id_user=user_id,id_exercise=id_exercise,judge_status=value)

    db.session.add(attempt)

    db.session.commit()

    answerOut = str(clearResult)  + ": " + value

    print ("[WEB] %s\n" % answerOut)

    return render_template('exercise_result.html', title=title, result=answerOut)
