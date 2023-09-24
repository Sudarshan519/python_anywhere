from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sshtunnel
import mysql.connector
 
import MySQLdb
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0
url="mysql+mysqlconnector://SudarshanShresth:Asmir123@SudarshanShrestha.mysql.pythonanywhere-services.com/SudarshanShresth$default"
with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username='SudarshanShresth', ssh_password='Asmir123',
    remote_bind_address=('SudarshanShrestha.mysql.pythonanywhere-services.com', 3306)
) as tunnel: 
    tunnel.start()
    try:
      mydb = mysql.connector.connect(
      host="127.0.0.1",
      user="SudarshanShresth",
      password="Asmir123",
      database="SudarshanShresth$JOBSEARCH",
 
      )

      mycursor = mydb.cursor()
      print("connected")
      mycursor.execute("SHOW DATABASES")
      print("query executed")
      for x in mycursor:
          print(x) 
    except Exception as e:
        print(e)

    # connection = MySQLdb.connect(
    #     user='SudarshanShresth',
    #     password='',
    #     host='127.0.0.1', port=tunnel.local_bind_port,
    #     db='SudarshanShresth$JOBSEARCH',
    # )
    # connection.execute("SHOW DATABASES")
    #     host="SudarshanShrestha.mysql.pythonanywhere-services.com",
    # user="SudarshanShresth",
    # password="Asmir123",
    # database="SudarshanShresth$JOBSEARCH"
# tunnel=sshtunnel.SSHTunnelForwarder(
#   ('ssh.pythonanywhere.com'),ssh_username='SudarshanShrestha',ssh_password='Asmir123',
#     remote_bind_address=('SudarshanShrestha.mysql.pythonanywhere-services.com',3306)
# )
# tunnel.start()
# DATABASE_URL_PYTHON ="mysql://SudarshanShresth:Asmir123@127.0.0.1:{}/SudarshanShresth$default".format(tunnel.local_bind_port)
 

# # def create_app():
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_PYTHON

# with app.app_context():
#     db = SQLAlchemy(app)  
#     db.create_all()

