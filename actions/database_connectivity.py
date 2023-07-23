import mysql.connector

def ExecuteQuery(query):
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Kushal123",
        database="chatbot"
    )
    # print(query)
    mycursor=mydb.cursor()
    mycursor.execute(query)
    mydb.commit()

def ReturnQueryOne(query):
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Kushal123",
        database="chatbot"
    )
    print(query)
    mycursor=mydb.cursor()
    mycursor.execute(query)
    returned_value=mycursor.fetchone()
    print(returned_value)
    return returned_value

def ReturnQueryAllNames(query):
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Kushal123",
        database="chatbot"
    )
    print(query)
    mycursor=mydb.cursor()
    mycursor.execute(query)
    all_names = [row[0] for row in mycursor.fetchall()]
    print(all_names)
    return all_names

def ReturnQueryAllCourses(query):
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Kushal123",
        database="chatbot"
    )
    print(query)
    mycursor=mydb.cursor()
    mycursor.execute(query)
    all_courses= mycursor.fetchall()
    print(all_courses)
    return all_courses
