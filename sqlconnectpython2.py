import mysql.connector
import sshtunnel
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0
with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username='SudarshanShrestha', ssh_password='Asmir123',
    remote_bind_address=('SudarshanShrestha.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    try:
     mydb = mysql.connector.connect(
     host="127.0.0.1",
     user="SudarshanShresth",
     password="test",
     database="SudarshanShresth$JOBSEARCH",
     port=tunnel.local_bind_port
     )#

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
    #     password='Asmir123',
    #     host='127.0.0.1', port=tunnel.local_bind_port,
    #     db='SudarshanShresth$JOBSEARCH',
    # )

try:
    mydb = mysql.connector.connect(
    host="SudarshanShrestha.mysql.pythonanywhere-services.com",
    user="SudarshanShresth",
    password="Asmir123",
    database="SudarshanShresth$JOBSEARCH"

    )

    mycursor = mydb.cursor()
    print("connected")
    mycursor.execute("SHOW DATABASES")
    print("query executed")
    for x in mycursor:
        print(x)
except Exception as e:
    print(e)
