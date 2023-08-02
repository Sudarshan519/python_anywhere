
# A very simple Flask Hello World app for you to get started with...

# from socket import gethostname
import sys
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
import os
from sqlalchemy.sql import func
# from sqlalchemy_serializer import SerializerMixin
# from dataclasses import dataclass 
# from flask_serialize import FlaskSerialize
#DATABASE_URL_PYTHON ="mysql+mysqlconnector://sudarshanshresth:Asmir123@SudarshanShrestha.mysql.pythonanywhere-services.com/SudarshanShresth$default"#.format(5432)#tunnel.local_bind_port)
# DATABASE_URL_PYTHON ="mysql+mysqlconnector://sudarshanshresth:Asmir123@SudarshanShrestha.mysql.pythonanywhere-services.com/SudarshanShresth$default"#.format(5432)#tunnel.local_bind_port)

# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_PYTHON
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 300  # For example, set to 30 seconds

# db = SQLAlchemy(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_PYTHON
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  
# fs_mixin = FlaskSerialize(db)
path = '/home/SudarshanShrestha/mysite'
if path not in sys.path:
   sys.path.insert(0, path)

# from flask_app import app  

# @app.route('/')
# def home():
#     # etc etc, flask app code
#     return {"response":"Hello  world"}

# class CustomSerializerMixin(SerializerMixin):
#     serialize_types = (
#         (id, lambda x: str(x)),
#     )

    
class Student(db.Model):
#     serialize_only = ('id', 'email_id', 'role_type', 'users.id')
    
#     serialize_rules = ('-merchants')
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'
  
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)


# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     return render_template('create.html')

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          age=age,
                          bio=bio)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', student=student)
# @app.route('/student/<int:item_id>')
# @app.route('/students', methods=['GET', 'POST'])
# def all_students(item_id=None):
#     students=Student.query.all()
#     # return Item.fs_get_delete_put_post(item_id)
#     return Student.fs_get_delete_put_post(item_id)
@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # db.create_all()
    # if 'liveconsole' not in gethostname():
#        app.run(host='0.0.0.0',debug=True)
        app.run(debug=True)
