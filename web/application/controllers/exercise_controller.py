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
from sqlalchemy import func
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf8')

@app.route('/exercise_list/<string:level>', methods=['GET', 'POST'])
@app.route('/exercise_list/', defaults={"level": None}, methods=['GET', 'POST'])
@login_required
def exercise_list(level=None):

    exercises = db.session.query(Exercise.id, Exercise.exercise_number, Exercise.name, Exercise.level). \
    filter(Exercise.level == level).all()

    done_exercises = db.session.query(Attempt.id_exercise, Attempt.status). \
    filter(Attempt.id_user == current_user.id, Attempt.status == 'Status 5'). \
    group_by(Attempt.status, Attempt.id_exercise).order_by(Attempt.id_exercise).all()

    undone_exercises = db.session.query(Attempt.id_exercise, Attempt.status). \
    filter(Attempt.id_user == current_user.id, Attempt.status != 'Status 5'). \
    group_by(Attempt.status, Attempt.id_exercise).order_by(Attempt.id_exercise).all()

    list_done = []

    list_undone = []

    for item in done_exercises:

        list_done.append(item.id_exercise)

    for item in undone_exercises:

        if item.id_exercise not in list_done:

            list_undone.append(item.id_exercise)

    return render_template('exercise_list.html', exercises_list=exercises, done_exercises=list_done, undone_exercises=list_undone)

@app.route('/exercisegroup')
@login_required
def exercisegroup():

    return render_template('exercise_group.html')

@app.route('/judges/<int:exercise>', methods=['GET', 'POST'])
@app.route('/judges/', defaults={"exercise": None}, methods=['GET', 'POST'])
@login_required
def judges(exercise):

    exercises = Exercise.query.order_by(Exercise.exercise_number.asc()).all()

    return render_template('judge_exercises.html', exercises_list=exercises, exercise=exercise)

@app.route('/previewexercise/<int:exercise>', methods=['GET', 'POST'])
@app.route('/previewexercise/', defaults={"exercise": None}, methods=['GET', 'POST'])
@login_required
def previewexercise(exercise):

    exercise = Exercise.query.filter_by(exercise_number=exercise).first()

    return render_template('preview_exercise.html', exercise=exercise)

@app.route('/registercode', methods=['GET', 'POST'])
@login_required
def registercode():

    user_code = request.form.get('codearea')

    exercise_number = request.form.get('exercise_number')

    user_language = request.form.get('language')

    id_user = current_user.id

    exercise = Exercise.query.filter_by(exercise_number=exercise_number).first()

    id_exercise = exercise.id

    judge = Judge(code=user_code, language=user_language, id_exercise=id_exercise, id_user=id_user)

    db.session.add(judge)

    db.session.commit()

    # Start to create the user code file to compile
    date_time = (time.strftime("%d%m%Y") + "_" + time.strftime("%H%M%S"))

    base_compiler_dir = (os.getcwd().replace("web", "")) + "compiler/"

    exec_dir = base_compiler_dir + "compiler.py"

    user_file_dir = base_compiler_dir + "tojudge/" + exercise_number + "_" + \
    date_time + "_" + str(id_user) + "." + user_language

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

    print "[WEB] Result: %s\n" % result

    if result.find('Status 1') != -1:

        #Insert the new tries and the user status (error or accept)
        new_attempt = Attempt(id_exercise=id_exercise, id_user=id_user, tries=1, errors=1, accepts=0, status="Status 1")

        db.session.add(new_attempt)

        db.session.commit()

        return render_template('exercise_result.html', \
        result="Status 1: Erro de sintaxe", result_error=result)

    else:

        clearesult = str(result).strip()

        if clearesult == "Status 5":

            #Insert the new tries and the user status (error or accept)
            new_attempt = Attempt(id_exercise=id_exercise, id_user=id_user, tries=1, errors=0, accepts=1, status=clearesult)

        else:

            #Insert the new tries and the user status (error or accept)
            new_attempt = Attempt(id_exercise=id_exercise, id_user=id_user, tries=1, errors=1, accepts=0, status=clearesult)

        db.session.add(new_attempt)

        db.session.commit()

        #Set the Key/value based on result
        status = {'Status 1':'Erro de sintaxe', 'Status 2':'Resposta incorreta', 'Status 3':'Tempo limite excedido', 'Status 4':'Erro de apresentacao', 'Status 5':'Codigo submetido com sucesso'}

        if status.has_key(clearesult):

            value = status[clearesult]

        else:

            value = ""

        answerout = str(clearesult)  + ": " + value

        return render_template('exercise_result.html', result=answerout)

@app.route('/exercise_statistics', methods=['GET', 'POST'])
def exercise_statistics():

    cursor = db.session.query(func.sum(Attempt.tries)).filter(Attempt.id_user==id_user)

    tries = cursor.scalar()

@app.route('/test')
def test():

    exercises = Exercise.query.all()

    return render_template('modal_exercises.html', exercises=exercises)
