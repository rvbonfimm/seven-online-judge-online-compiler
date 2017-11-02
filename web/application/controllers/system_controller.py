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

@app.route('/functionality')
def functionality():

    title = "Funcionalidades"

    return render_template('functionality.html', title=title)

@app.route('/rules', methods=['GET', 'POST'])
def rules():

    return render_template('rules.html')
