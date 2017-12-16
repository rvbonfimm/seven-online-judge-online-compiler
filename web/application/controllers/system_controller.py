# encoding=utf8

from application import app
from flask import render_template
from flask_login import login_required, current_user

@app.route('/')
@app.route('/index')
def index():

    title = "Seven Online Judge"

    if current_user.is_authenticated:

        return render_template('main.html', title=title)

    else:

        return render_template('index.html', title=title)


@app.route('/presentation')
@login_required
def presentation():

    title = "Apresentacao"

    return render_template('presentation.html', title=title)


@app.route('/main')
@login_required
def main():

    title = "Pagina principal"

    return render_template('main.html', title=title)

@app.route('/studyboard')
@login_required
def studyboard():

    return render_template('study_board_main.html')

@app.route('/exerciseboard')
@login_required
def exerciseboard():

    return render_template('exercise_board_main.html')

@app.route('/systemboard')
@login_required
def systemboard():

    return render_template('system_board_main.html')

@app.route('/functionality')
def functionality():

    title = "Funcionalidades"

    return render_template('functionality.html', title=title)

@app.route('/rules', methods=['GET', 'POST'])
def rules():

    return render_template('rules.html')

@app.route('/why_svoj', methods=['GET', 'POST'])
def why_svoj():

    return render_template('why_svoj.html')