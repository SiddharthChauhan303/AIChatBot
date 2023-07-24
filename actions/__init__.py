# import sys
# import pandas as pd
# sys.path.append('/Users/kushalpartani/Desktop/Course-Registration-Bot/actions')

# import database_connectivity as dbc
# def checkprogram(roll):
#         if (roll[:3] == "IMT"):
#             program="IMTech"
#         elif (roll[:2]=="PH"):
#             program="PhD"
#         elif(roll[:2]== "MT"):
#             program="MTech"
#         elif(roll[:2]=="MS"):
#             program="MS"
#         elif(roll[:2]=="DT"):
#             program="DT"
#         else:
#             program="None"
#         return program


# def insert(name,roll):
#     program=checkprogram(roll)
#     dbc.ExecuteQuery('INSERT into student_details values("'+roll+'","'+name+'","'+program+'")')

# file="/Users/kushalpartani/Desktop/Course-Registration-Bot/actions/Student_Details.xlsx"
# file2="/Users/kushalpartani/Desktop/Course-Registration-Bot/actions/Courses.xlsx"
# file3="/Users/kushalpartani/Desktop/Course-Registration-Bot/actions/Profs.xlsx"
# data=pd.read_excel(file)
# data1=pd.read_excel(file2)
# data2=pd.read_excel(file3)
# names=data["Full Name"]
# roll=data["Roll Number"]
# Course_name=data1["Elective name"]
# Specialization=data1["Specialization"]
# Pre_requisites=data1["Pre-requisites"]
# Faculty_name=data1["Faculty Name"]
# Faculty_code=data1["Faculty"]
# Course_code=data1["Course Code"]
# diff=data1["Difficulty"]
# prog=data1["Program"]
# Profs=data2["Faculty"]
# Prof_code=data2["Faculty Codes"]
# about=data2["About"]

# for i in range(len(names)):
#     # insert(names[i],roll[i])

# for i in range(len(Course_name)):
#     query='INSERT into course_details values("'+str(Course_name[i])+'","'+str(Course_code[i])+'","'+str(Faculty_name[i])+'","'+str(Faculty_code[i])+'","'+str(Specialization[i])+'","'+str(diff[i])+'","'+str(prog[i])+'","'+str(Pre_requisites[i])+'")'
#     dbc.ExecuteQuery(query)

# for i in range(len(Profs)):
#      dbc.ExecuteQuery('INSERT into professor_details values("'+str(Profs[i])+'","'+str(Prof_code[i])+'","'+str(about[i])+'")')


