from application import db
from datetime import datetime

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(40), unique=True)

    password = db.Column(db.String(150))

    name = db.Column(db.String(30))

    lastname = db.Column(db.String(40))

    email = db.Column(db.String(120), unique=True)

    gender = db.Column(db.String(10))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id) #if python 3, return a str - python 3 use unicode for strings

    def __init__(self, username, password, name, lastname, email, gender):

        self.username=username
        self.password=password
        self.name=name
        self.lastname=lastname
        self.email=email
        self.gender=gender

class Exercise(db.Model):

    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)

    exercise_number = db.Column(db.Integer, unique=True)

    name = db.Column(db.String(40), unique=True)

    description = db.Column(db.Text)

    level = db.Column(db.Integer)

    date_created = db.Column(db.DateTime)

    inputt = db.Column(db.String(100))

    outputt = db.Column(db.String(100))

    input_description = db.Column(db.String(100))

    output_description = db.Column(db.String(100))

    def __init__(self, exercise_number, name, description, level, inputt, outputt, input_description, output_description, date_created=None):

        self.exercise_number = exercise_number
        self.name = name
        self.description = description
        self.level = level

        if date_created == None:
            date_created = datetime.utcnow()
        else:
            self.date_created = date_created

        self.inputt = inputt
        self.outputt = outputt
        self.input_description = input_description
        self.output_description= output_description

class Attempt(db.Model):

    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key=True)
    id_exercise = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    tries = db.Column(db.Integer)
    errors = db.Column(db.Integer)
    accepts = db.Column(db.Integer)
    status = db.Column(db.String(10))

    def __init__(self, id_exercise, id_user, tries, errors, accepts, status):

        self.id_exercise=id_exercise
        self.id_user=id_user
        self.tries=tries
        self.errors=errors
        self.accepts=accepts
        self.status=status

class Judge(db.Model):

    __tablename__ = 'judges'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    language = db.Column(db.String(10))
    id_exercise = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    #user_information = db.Relationship('User', foreign_keys=id_user)

    def __init__(self, code, language, id_exercise, id_user):

        self.code=code
        self.language=language
        self.id_exercise=id_exercise
        self.id_user=id_user

class Study(db.Model):

    __tablename__ = 'studies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):

        self.name = name


class UserPlan(db.Model):

    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_study = db.Column(db.Integer, db.ForeignKey('studies.id'))
    status = db.Column(db.Integer)
    
    def __init__(self, id_user, id_study, status):

        self.id_user = id_user
        self.id_study = id_study
        self.status = status
