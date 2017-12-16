# encoding=utf8
import re
import json

from application import app, db
from flask import render_template, request, send_file, redirect, url_for
from flask_login import login_user, login_required, current_user
from application.models.tables import Exercise, Study, UserPlan, Study_Statistic


@app.route("/study_material_download", methods=['GET'])
def studymaterialdownload():

    return render_template('study_material_download.html')

@app.route("/download_study_file/Module_1")
def downloadfile_module_1():

    return send_file("/home/eliseuvidaloca/Desktop/development/sevenonlinejudge/web/application/static/files/Material-de-Apoio-Modulo-1.pdf", attachment_filename="Material-de-Apoio-Modulo-1.pdf")

@app.route("/download_study_file/Module_2")
def downloadfile_module_2():

    return send_file("/home/eliseuvidaloca/Desktop/development/sevenonlinejudge/web/application/static/files/Material-de-Apoio-Modulo-2.pdf", attachment_filename="Material-de-Apoio-Modulo-2.pdf")

@app.route("/study_explanation", methods=['GET'])
def studyexplanation():

    return render_template('study_explanation.html')

@app.route("/interactive_study/<int:id_study>", methods=['GET', 'POST'])
@app.route("/interactive_study/", defaults={'id_study': None}, methods=['GET', 'POST'])
def interactivestudy(id_study=None):

    if request.method == 'GET':

        study_item = db.session.query(Study.id, Study.name, Study.type_study, \
            Study.content, Study.exercises, Study.explanation, Study.helper, \
            Study.regex).filter(Study.id == id_study).first()

        return render_template('interactive_study.html', study_item=study_item)

    elif request.method == 'POST':

        user_data = request.form.get('user_code')

        user_code_status = validate_user_data(user_data, id_study)

        if  user_code_status[2] != user_code_status[3]:

            warning_message = "Alguns itens não foram validados."

            return render_template('interactive_study.html', indexes=user_code_status[0], user_data=user_code_status[1], validation_itens=user_code_status[2], validated_itens=user_code_status[3], warning_message=warning_message)

        else:

            info_message = "Todos os itens foram validados."

            return render_template('interactive_study.html', indexes=user_code_status[0], user_data=user_code_status[1], validation_itens=user_code_status[2], validated_itens=user_code_status[3], info_message=info_message)

@app.route("/interactive_study_explanation", methods=['GET'])
def interactivestudyexplanation():

    study_list = db.session.query(Study.id, Study.name).order_by(Study.id).all()

    return render_template('interactive_study_explanation.html', study_itens=study_list)

@app.route('/startuser', methods=['GET','POST'])
@login_required
def startuser():

    if request.method == 'POST':

        user_experience = request.form['programming_experience']

        study_itens = Study.query.all()

        checkRegisteredPlan = db.session.query(UserPlan.id_user).filter_by(id_user=current_user.id).first() is not None

        if user_experience == "no":

            if not(checkRegisteredPlan):

                for item in study_itens:

                    new_plan = UserPlan(id_user=current_user.id, id_study=item.id)

                    db.session.add(new_plan)

                db.session.commit()

                return render_template('study_explanation.html')

            else:

                return redirect(url_for('studyplan'))
                
        elif user_experience == "yes":

            if not(checkRegisteredPlan):

                return render_template('presentation_next.html', study_itens=study_itens)

            else:

                return redirect(url_for('studyplan'))

    elif request.method == 'GET':

        return render_template('presentation.html')

@app.route('/startusernext', methods=['GET','POST'])
@login_required
def startusernext():

    if request.method == 'POST':

        study_itens = request.form.getlist('studyitens')

        unknownItens = Study.query.filter(Study.name.in_(study_itens))

        checkRegisteredPlan = db.session.query(UserPlan.id_user).filter_by(id_user=current_user.id).first() is not None

        if not(checkRegisteredPlan):

            for item in unknownItens:

                new_plan = UserPlan(id_user=current_user.id, id_study=item.id)

                db.session.add(new_plan)

            db.session.commit()

            return render_template('study_explanation.html')

        else:

            return redirect(url_for('studyplan'))

    elif request.method == 'GET':

        return render_template('presentation_next.html')

@app.route("/study_plan")
def studyplan():

    list_out = []

    study_itens = db.session.query(Study.id, Study.name, Study.type_study, \
        Study.content, Study.exercises, Study.explanation, Study.helper, Study.regex). \
        join(UserPlan, Study.id == UserPlan.id_study). \
        filter(UserPlan.id_user == current_user.id). \
        group_by(UserPlan.id_study). \
        order_by(Study.id).all()

    for item in study_itens:

        aux = db.session.query(Study_Statistic.accepts, Study_Statistic.errors).\
        filter(Study_Statistic.id_study == item.id, Study_Statistic.id_user == current_user.id).\
        group_by(Study_Statistic.accepts, Study_Statistic.errors).all()

        flag_accept = False
        flag_error = False

        if aux:

            for statistic in aux:

                if statistic.accepts == 1:

                    flag_accept = True

                if statistic.errors == 1:

                    flag_error = True

        if flag_accept:

            output = "accepted"

        elif flag_error:

            output = "error"

        else:

            output = "null"

        data = {
            'id_study': item.id,
            'name': item.name,
            'type_study': item.type_study,
            'status': output
        }

        list_out.append(data)

    return render_template('study_plan.html', list_data=list_out)

def validate_user_data(data, id_study):

    regex_to_validate = db.session.query(Study.regex).filter(Study.id == id_study).one()

    regex_out = []

    index_output = []

    matched_objects = []

    splitted_regex = str(regex_to_validate.regex).split('\n')

    splitted_data = data.split('\r\n')

    quantity_itens_validation = len(splitted_regex)

    for data, regex in zip(splitted_data, splitted_regex):

        match = re.match(regex, data)

        if match:

            index_output.append(str(match.start()) + ";" + str(match.end()))

            matched_objects.append(match.group(0))

        else:

            index_output.append('')

    quantity_itens_validated = len(matched_objects)

    if quantity_itens_validation != quantity_itens_validated:

        #Specify that the study was not completed
        accepts = "0"

        errors = "1"

    else:

        #Specify that the study was completed
        accepts = "1"

        errors = "0"

    new_statistic = Study_Statistic(tries="1", accepts=accepts, errors=errors, id_study=id_study, id_user=current_user.id)

    db.session.add(new_statistic)

    db.session.commit()

    return [index_output, matched_objects, quantity_itens_validation, quantity_itens_validated]
