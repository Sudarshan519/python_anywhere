import mysql.connector

try:
    mydb = mysql.connector.connect(
    host="SudarshanShrestha.mysql.pythonanywhere-services.com",
    user="SudarshanShresth",
    password="Asmir123",
    database="SudarshanShresth$default"
    
    )

    mycursor = mydb.cursor()
    print("connected")
    mycursor.execute("SHOW DATABASES")
    print("query executed")
    for x in mycursor:
        print(x) 
except Exception as e:
    print(e)
