# encoding=utf8
import re

from application import app, db
from flask import render_template, request, send_file
from flask_login import login_user, login_required, current_user
from application.models.tables import Exercise, Study, UserPlan


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

        user_code_status = validate_user_data(user_data)

        return render_template('interactive_study.html', result=user_code_status)

@app.route("/interactive_study_explanation", methods=['GET'])
def interactivestudyexplanation():

    study_list = db.session.query(Study.id, Study.name).order_by(Study.id).all()

    return render_template('interactive_study_explanation.html', study_itens=study_list)

@app.route('/startuser', methods=['GET','POST'])
@login_required
def startuser():

    if request.method == 'POST':

        user_experience = request.form['programming_experience']

        unknownItens = Study.query.all()

        checkRegisteredPlan = db.session.query(UserPlan.id_user).filter_by(id_user=current_user.id).first() is not None

        if user_experience == "no":

            if (checkRegisteredPlan):

                return render_template('study_plan.html')                

            else:

                for item in unknownItens:

                    new_plan = UserPlan(id_user=current_user.id, id_study=item.id, status="0")

                    db.session.add(new_plan)

                db.session.commit()

                return render_template('study_plan.html', study_itens=unknownItens)

        elif user_experience == "yes":

            if (checkRegisteredPlan):

                return render_template('study_plan.html')

            else:

                return render_template('presentation_next.html', study_itens=unknownItens)

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

                new_plan = UserPlan(id_user=current_user.id, id_study=item.id, status="0")

                db.session.add(new_plan)

            db.session.commit()

            return render_template('study_plan.html', study_itens=unknownItens)

        else:

            #message = "Você já possui um Plano de Estudos definido. Para alterá-lo, vá até a Guia de Estudos/Planos."

            return render_template('study_plan.html')

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

def validate_user_data(data):

    regex_to_validade = '(char [\w]+\[[\d]+\];)\n(char [\w]+\[[\d]+\];)\n(int [\w]+;)\n(char [\w]+\[[\d]+\];)\n(char [\w]+\[[\d]+\];)'

    #regex = db.session.query(Study.regex).filter(Study.id)

    splitted_regex = regex_to_validade.split('\n')

    splitted_data = data.split('\r\n')

    index_output = []

    for data, regex in zip(splitted_data, splitted_regex):

        match = re.match(regex, data)

        if match:

            index_output.append(str(match.start()) + ";" + str(match.end()))

        else:

            index_output.append('')

    return index_output