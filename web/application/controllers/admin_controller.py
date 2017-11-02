import os
from application import app, db
from flask import render_template, request, url_for

from flask_login import login_user, login_required
from application.models.tables import Exercise, Study

@app.route('/admin/registerExercise', methods=['GET','POST'])
@login_required
def registerexercise():

    if(request.method == 'POST'):

        exercise_number = request.form.get('exercise_number')

        name = request.form.get('name')

        description = request.form.get('description')

        level = request.form.get('level')

        inputt = request.form.get('input')

        outputt = request.form.get('output')

        input_description = request.form.get('input_description')

        output_description = request.form.get('output_description')

        new_exercise = Exercise(exercise_number=exercise_number, name=name, description=description, level=level, inputt=inputt, outputt=outputt, input_description=input_description, output_description=output_description)

        db.session.add(new_exercise)

        db.session.commit()

        message = "New exercise was successfully inserted at the db.\n"

        return render_template('main.html', message=message)

    elif(request.method == 'GET'):

        return render_template('create_exercise.html')


@app.route('/admin/new_study', methods=['GET', 'POST'])
@login_required
def new_study():

    if request.method == 'POST':

        name = request.form['name']

        new_study = Study(name=name)

        db.session.add(new_study)

        db.session.commit()

        message = "New study was added successfully."

        return render_template('main.html', message=message)

    elif request.method == 'GET':

        return render_template('new_study.html')

@app.route('/admin/generatefileexercise', methods=['GET', 'POST'])
def generatefileexercise():

    list_exercises = db.session.query(Exercise.exercise_number, Exercise.inputt, Exercise.outputt). \
    order_by(Exercise.exercise_number).all()

    for exercise in list_exercises:

        print exercise.exercise_number

        if not file_exists(exercise.exercise_number):

            exercise_dir_input = os.getcwd().replace("web", "compiler") + "/exercises/input/"

            exercise_dir_output = os.getcwd().replace("web", "compiler") + "/exercises/output/"

            fileinput = exercise_dir_input + str(exercise.exercise_number) + ".exercisein"

            fileoutput = exercise_dir_output + str(exercise.exercise_number) + ".exerciseout"

            print "Fileinput: %s\n" % fileinput

            print "Fileoutput: %s\n" % fileoutput

            with open(fileinput, 'w') as fh_input:

                fh_input.write(exercise.inputt)

                fh_input.write('\n')

            fh_input.close()

            with open(fileoutput, 'w') as fh_output:

                fh_output.write(exercise.outputt)

                fh_output.write('\n')

            fh_output.close()

    return "Files created successfully."

def file_exists(exercise):

    input_exercise_dir = os.getcwd().replace('web', 'compiler') + \
    str('/exercises/input/') + str(exercise) + '.exercisein'

    output_exercise_dir = os.getcwd().replace('web', 'compiler') + \
    str('/exercises/output/') + str(exercise) + '.exerciseout'

    if not(os.path.isfile(input_exercise_dir) and os.path.isfile(output_exercise_dir)):

        return False

    return True