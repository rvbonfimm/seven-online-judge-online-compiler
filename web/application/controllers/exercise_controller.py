# encoding=utf8  

import sys  
import pexpect
import time
import os, os.path
import ast

from application import app, db
from flask import render_template, request
from pexpect import spawn
from flask_login import login_user, login_required, current_user
from application.models.tables import Exercise, Judge, User, Attempt, Exercise_Statistic
from sqlalchemy import func
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf8')

@app.route('/exercise_list/<string:level>', methods=['GET', 'POST'])
@app.route('/exercise_list/', defaults={"level": None}, methods=['GET', 'POST'])
@login_required
def exerciselist(level=None):

    exercises = db.session.query(Exercise.id, Exercise.exercise_number, Exercise.name, \
    Exercise.level).filter(Exercise.level == level). \
    order_by(Exercise.exercise_number).all()

    return render_template('exercise_list.html', exercises_list=exercises)

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

    number = request.form.get('exercise_number')

    user_language = request.form.get('language')

    id_user = current_user.id

    exercise = db.session.query(Exercise.id). \
    filter(Exercise.exercise_number == number).first()

    id_exercise = exercise.id

    judge = Judge(code=user_code, language=user_language, id_exercise=id_exercise, id_user=id_user)

    db.session.add(judge)

    db.session.commit()

    # Start to create the user code file to compile
    date_time = (time.strftime("%d%m%Y") + "_" + time.strftime("%H%M%S"))

    base_compiler_dir = (os.getcwd().replace("web", "")) + "compiler/"

    exec_dir = base_compiler_dir + "compiler.py"

    user_file_dir = base_compiler_dir + "tojudge/" + number + "_" + \
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

    print result

    dict_result = ast.literal_eval(result)

    if dict_result.has_key('Status'):

        status = dict_result['Status']
 
        time_ran = dict_result['Time']

    else:

        return "Something went wrong at Key's dictionary result. Contact the Admin, please."

    if result.find('Status 1') != -1:

        result = "Status 1"

        #Insert the new tries and the user status (error or accept)
        new_statistic = Exercise_Statistic(id_exercise=id_exercise, id_user=id_user, tries=1, \
        errors=1, accepts=0, status=result)

        db.session.add(new_statistic)

        db.session.commit()

        increment_exercise(id_exercise, result)

        increment_attempt(id_exercise, result)

        return render_template('exercise_result.html', \
        result="Status 1: Erro de sintaxe", result_error=result, time=time_ran, code_used=user_code)

    elif status == 'Status 2' or status == 'Status 3' or status == 'Status 4':
    
        #Insert the new tries and the user status (error or accept)
        new_statistic = Exercise_Statistic(id_exercise=id_exercise, id_user=id_user, \
        tries=1, errors=1, accepts=0, status=status)

    elif status == 'Status 5':

        #Insert the new tries and the user status (error or accept)
        new_statistic = Exercise_Statistic(id_exercise=id_exercise, id_user=id_user, \
        tries=1, errors=0, accepts=1, status=status)

    else:

        return "Error: result " + str(status) + " not expected. Contant the admin, please."

        return render_template('exercise_result.html', result_error=result, time=time_ran, code_used=user_code)

    increment_exercise(id_exercise, status)

    increment_attempt(id_exercise, status)

    db.session.add(new_statistic)

    db.session.commit()

    additional_status = {'Status 1':'Erro de sintaxe', 'Status 2':'Resposta incorreta', \
    'Status 3':'Tempo limite excedido', 'Status 4':'Erro de apresentacao', \
    'Status 5':'Codigo submetido com sucesso'}

    if additional_status.has_key(status):

        value = additional_status[status]

    else:

        error_message = "Any key was found at status exercise dictionary. Admin, fix it!\n"

        return render_template('exercise_result.html', error_message=error_message, time=time_ran, code_used=user_code)

    answerout = str(status)  + ": " + value

    return render_template('exercise_result.html', result=answerout, time=time_ran, code_used=user_code)

@app.route('/exercise_statistics', methods=['GET', 'POST'])
def exercise_statistics():

    return "ok"

def increment_exercise(id_exercise, status):

    try:

        db.session.query(Exercise).filter(Exercise.id == id_exercise). \
        update({Exercise.tries: Exercise.tries + 1})

        if status == 'Status 5':

            db.session.query(Exercise).filter(Exercise.id == id_exercise). \
            update({Exercise.accepts: Exercise.accepts + 1})

        elif status != 'Status 5':

            db.session.query(Exercise).filter(Exercise.id == id_exercise). \
            update({Exercise.errors: Exercise.errors + 1})

        return True

    except Exception, e:

        print "Exception at increment: " + str(e)

        return False

def increment_attempt(id_exercise, status):

    try:

        #Search for already registered id_exercise at db
        check = db.session.query(Attempt.id_exercise, Attempt.status). \
        filter(Attempt.id_exercise == id_exercise, Attempt.status == status). \
        order_by(Attempt.id_exercise). \
        all()

        if not check:

            new_attempt = Attempt(status=status, id_exercise=id_exercise, id_user=current_user.id)
            db.session.add(new_attempt)
            db.session.commit()

        else:

            #Registered before - check if the new status is Status 5: if yes, update. if not, if new status is diff of last, update
            for column in check:

                exercise = column.id_exercise
                db_status = column.status

            #Status registered at database is Status 5(code accepted - do not need to change)
            if db_status == 5:

                return

            else:

                # If new status if equal to saved status at database, not necessary to update
                if db_status == status:

                    return

                else:

                    db.session.query(Attempt).filter(Attempt.id_exercise == id_exercise). \
                    update({Attempt.status: status})

    except Exception, e:

        print e

@app.route("/status_explanation", methods=['GET'])
def statusexplanation():

    return render_template("status_explanation.html")