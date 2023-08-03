from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sshtunnel
import mysql.connector
tunnel=sshtunnel.SSHTunnelForwarder(
  ('ssh.pythonanywhere.com'),ssh_username='SudarshanShrestha',ssh_password='Asmir123',
    remote_bind_address=('SudarshanShrestha.mysql.pythonanywhere-services.com',3306)
)
tunnel.start()
DATABASE_URL_PYTHON ="mysql://sudarshanshrestha:test@127.0.0.1:{}/SudarshanShresth$default".format(tunnel.local_bind_port)
 

# def create_app():
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_PYTHON

with app.app_context():
    db = SQLAlchemy(app)  
    db.create_all()

