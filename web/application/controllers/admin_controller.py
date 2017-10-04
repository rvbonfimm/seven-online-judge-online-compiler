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

        if inputt == "":

            inputt = "Vazio"

        output = request.form.get('output')

        new_exercise = Exercise(exercise_number=exercise_number, name=name, description=description, level=level, input=inputt, output=output)

        db.session.add(new_exercise)

        db.session.commit()

        message = "New exercise was successfully inserted at the db.\n"

        return render_template('index.html', message=message)

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