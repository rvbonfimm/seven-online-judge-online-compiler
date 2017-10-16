# encoding=utf8  

import sys  
import pexpect
import time
import os

from application import app, db
from flask import render_template, request, url_for
from pexpect import spawn
from flask_login import login_user, login_required, current_user
from application.models.tables import Exercise, Judge, User, Attempt


reload(sys)
sys.setdefaultencoding('utf8')

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

    title = "Julgamento de Exercicios"

    user_code = request.form.get('codearea')

    exercise_number = request.form.get('exercise_number')

    user_language = request.form.get('language')

    user_id = current_user.id

    exercise = Exercise.query.filter_by(exercise_number=exercise_number).first()

    id_exercise = exercise.id

    judge = Judge(code=user_code, language=user_language, id_exercise=id_exercise, id_user=user_id)

    db.session.add(judge)

    db.session.commit()

    # Start to create the user code file to compile
    date_time = (time.strftime("%d%m%Y") + "_" + time.strftime("%H%M%S"))

    base_compiler_dir = (os.getcwd().replace("web", "")) + "compiler/"

    exec_dir = base_compiler_dir + "compiler.py"

    user_file_dir = base_compiler_dir + "tojudge/" + exercise_number + "_" + \
    date_time + "_" + str(user_id) + "." + user_language

    user_file_dir = str(user_file_dir)

    with open(user_file_dir, "w") as userfile:

        userfile.write(user_code)

        userfile.close()

    cmd = ("python " + str(exec_dir) + " " + str(user_file_dir) + " -d")

    usercodeout = pexpect.spawn(cmd, timeout=7)

    index = usercodeout.expect([pexpect.EOF, pexpect.TIMEOUT])

    if index == 1:

        return "[WEB] Timeout exceeded.\n"

    result = usercodeout.before

    print("[WEB] Result: %s\n" % result)

    if result.find('Status 1') != -1:

        return render_template('exercise_result.html', title=title, \
        result="Status 1: Erro de sintaxe", result_error=result)

    else:

        clearesult = str(result).strip()

        status = {'Status 1':'Erro de sintaxe', 'Status 2':'Resposta incorreta', 'Status 3':'Tempo limite excedido', 'Status 4':'Erro de apresentacao', 'Status 5':'Codigo submetido com sucesso'}

        if status.has_key(clearesult):

            value = status[clearesult]

        else:

            value = ""

        answerout = str(clearesult)  + ": " + value

        return render_template('exercise_result.html', title=title, result=answerout)
