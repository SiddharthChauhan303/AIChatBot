import string
import random
import pandas as pd
import Levenshtein
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
    ActionExecutionRejected
)
import sys
import pandas as pd
sys.path.append('/Users/kushalpartani/Desktop/Course-Registration-Bot/actions')
import database_connectivity as dbc

class ActionDetails(Action):
    def name(self) -> Text:
        return "action_get_details"
    def checkprogram(roll):
        if (roll[:3] == "IMT"):
            program="IMtech"
        elif (roll[:2]=="PH"):
            program="PHD"
        elif(roll[:2]== "MT"):
            program="Mtech"
        elif(roll[:2]=="MS"):
            program="MS"
        elif(roll[:2]=="DT"):
            program="DT"
        else:
            program="None"
        return program
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        roll=tracker.get_slot("roll_number")
        # program=checkprogram(roll)
        if (roll[:3] == "IMT"):
            program="IMtech"
        elif (roll[:2]=="PH"):
            program="PHD" 
        elif(roll[:2]== "MT"):
            program="Mtech"
        elif(roll[:2]=="MS"):
            program="MS"
        elif(roll[:2]=="DT"):
            program="DT"
        else:
            program="None"

        query=f'SELECT name FROM student_details where rollnumber="{roll.upper()}"'
        print(roll.upper())
        name=dbc.ReturnQueryOne(query)
        if (program=="None"):
            dispatcher.utter_message(f"Your roll number is not correct. Please try again.")
            return[SlotSet("roll_number", None)]
        if name:
            dispatcher.utter_message(f"Your roll number is {roll} and name is {name[0]}.")
        else :
            dispatcher.utter_message("Your not registered please check your roll number")
            return[SlotSet("roll_number", None)]
        return [SlotSet("program",program),SlotSet("name",name[0])]



class ActionGetAllCourses(Action):
    def name(self) -> Text:
        return "action_get_all_courses"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        program=tracker.get_slot("program")
        dispatcher.utter_message(f"These are all the courses avaliable for your {program}")
        courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code,faculty_name,faculty_code from course_details  ")
        course_name=[]
        course_code=[]
        faculty_name=[]
        faculty_code=[]
        for i in range (len(courses)):
            course_name.append(courses[i][0])
            course_code.append(courses[i][1]) 
            faculty_name.append(courses[i][2])
            faculty_code.append(courses[i][3]) ##duplicate courses
        for i in range (len(courses)):
            dispatcher.utter_message(f"{i+1}. {course_name[i]}  -  {course_code[i]}, Taught by Prof {faculty_name[i]}, ({faculty_code[i]})")

        return []


class ActionGetFilteredCoursesBasedOnDomain(Action):
    def name(self) -> Text:
        return "action_get_filtered_courses_domain"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        program=tracker.get_slot("program")
        filter_type_domain=tracker.get_slot("filter_type_domain")
        filter_type_difficulty=tracker.get_slot("filter_type_difficulty")
        dispatcher.utter_message(f"These are all the courses filtered based on {filter_type_domain} avaliable for your {program}")
        if(filter_type_difficulty=="Beginner"):
            diff=1
        elif (filter_type_difficulty=="Intermediate"):
            diff=2
        elif(filter_type_difficulty=="Expert"):
            diff=3
        else:
            diff=0
        if filter_type_difficulty:
            courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code,faculty_name,faculty_code from course_details where specialization='{filter_type_domain}'and difficulty='{diff}' ")
        else:
            courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code,faculty_name,faculty_code from course_details where specialization='{filter_type_domain}' ")
        course_name=[]
        course_code=[]
        faculty_name=[]
        faculty_code=[]
        for i in range (len(courses)):
            course_name.append(courses[i][0])
            course_code.append(courses[i][1]) 
            faculty_name.append(courses[i][2])
            faculty_code.append(courses[i][3]) ##duplicate courses
        for i in range (len(courses)):
            dispatcher.utter_message(f"{i+1}. {course_name[i]}  -  {course_code[i]}, Taught by Prof {faculty_name[i]}, ({faculty_code[i]})")

        return []

class ActionGetFilteredCoursesBasedOnDifficulty(Action):
    def name(self) -> Text:
        return "action_get_filtered_courses_difficulty"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        program=tracker.get_slot("program")
        filter_type_difficulty=tracker.get_slot("filter_type_difficulty")
        prog=tracker.get_slot("program")
        domain=tracker.get_slot("filter_type_domain")
        if(filter_type_difficulty=="Beginner"):
            diff=1
        elif (filter_type_difficulty=="Intermediate"):
            diff=2
        elif(filter_type_difficulty=="Expert"):
            diff=3
        else:
            diff=0
        if(prog=="IMtech"):
            prog=1
        elif (prog=="Mtech"):
            prog=2
        elif(prog=="DT"):
            prog=3
        else:
            prog=0
        dispatcher.utter_message(f"These are all the courses filtered based on {filter_type_difficulty} avaliable for your {program}")
        if domain:
            if (prog==0):
                courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code,faculty_name,faculty_code from course_details where specialization='{domain}'")
            else:
                courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code,faculty_name,faculty_code from course_details where difficulty='{diff}'and specialization='{domain}' and program ='{prog}' or program='3' ")
        else:
            if (prog==0):
                courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code,faculty_name,faculty_code from course_details")
            else:
                courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code,faculty_name,faculty_code from course_details where difficulty='{diff}'and program ='{prog}' or program='3' ")
        
            if (prog==0):
                courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code,faculty_name,faculty_code from course_details")
            else:
                courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code,faculty_name,faculty_code from course_details where difficulty='{diff}'and program ='{prog}' or program='3' ")
        course_name=[]
        course_code=[]
        faculty_name=[]
        faculty_code=[]
        for i in range (len(courses)):
            course_name.append(courses[i][0])
            course_code.append(courses[i][1]) 
            faculty_name.append(courses[i][2])
            faculty_code.append(courses[i][3]) ##duplicate courses
        for i in range (len(courses)):
            dispatcher.utter_message(f"{i+1}. [Difficulty {filter_type_difficulty}]-{course_name[i]}  -  {course_code[i]}, Taught by Prof {faculty_name[i]}, ({faculty_code[i]})")

        # return [SlotSet("filter_type_domain",None)]
        return []



        
class ActionGetProfName1(Action):
    def name(self) -> Text:
        return "action_get_prof_name1"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        name=tracker.get_slot("prof_name")
        if not name:
            dispatcher.utter_message(text="Please provide a name.")
            return []
        query = f"SELECT faculty_name FROM professor_details;"
        query2= f"SELECT faculty_code FROM professor_details;"
        all_names=dbc.ReturnQueryAllNames(query)
        all_codes=dbc.ReturnQueryAllNames(query2)
        nearest_code=  min(all_codes, key=lambda name2: Levenshtein.distance(name2, name.upper()))
        nearest_name = min(all_names, key=lambda name2: Levenshtein.distance(name2, name))
        nearest_name2= all_names[all_codes.index(nearest_code)]
        d1=Levenshtein.distance(name,nearest_code)
        d2=Levenshtein.distance(name,nearest_name)
        prof=""
        choice=tracker.get_slot("expected_prof_name")
        if(d1<d2):
            if(choice==None):  
                dispatcher.utter_message("Do you mean Prof "+nearest_name2+" ?")
            prof=nearest_name2
        else:
            if(choice==None):
                dispatcher.utter_message("Do you mean Prof "+nearest_name+" ?")
            prof=nearest_name
        if(choice =="Yes" ):
            choice=""
            dispatcher.utter_message(f"What do you need about {prof}")
            return [SlotSet("actual_prof_name",prof),SlotSet("expected_prof_name",None)]
            
        elif(choice =="No"):
            choice=""
            dispatcher.utter_message("Sorry can't get that. Please try again!!")
            dispatcher.utter_message("What do you want to do?")
            return [SlotSet("prof_name",None),SlotSet("expected_prof_name",None)]

class ActionRemoveProfName(Action):
    def name(self) -> Text:
        return "action_remove_prof_name"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:   
        dispatcher.utter_message("Sorry can't get that. Please try again!!")
        return [SlotSet("prof_name",None)]

class ActionAboutProf(Action):
    def name(self) -> Text:
        return "action_get_about_details"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:   
        prof=tracker.get_slot("actual_prof_name")
        about=dbc.ReturnQueryOne(f"SELECT about from professor_details where faculty_name='{prof}' ")
        dispatcher.utter_message(about[0])
        return []
class ActionResetprof(Action):
    def name(self) -> Text:
        return "action_reset_prof_details"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:   
        dispatcher.utter_message("What do you want?")
        return [SlotSet("prof_name",None),SlotSet("actual_prof_name",None)]

class ActionGetCourseDetails(Action):
    def name(self) -> Text:
        return "action_get_courses_details"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:   
        prof=tracker.get_slot("actual_prof_name")
        courses=dbc.ReturnQueryAllCourses(f"SELECT course_name,course_code from course_details where faculty_name='{prof}' ")
        course_name=[]
        course_code=[]
        for i in range (len(courses)):
            course_name.append(courses[i][0])
            course_code.append(courses[i][1])  ##duplicate courses
        for i in range (len(courses)):
            dispatcher.utter_message(f"{course_name[i]}  -  {course_code[i]}")
        return []


class CustomActionCheckDomain(Action):
    def name(self) -> Text:
        return "action_check_domain"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:   
        specialization=tracker.get_slot("filter_type_domain")
        if specialization:
            return [FollowupAction("action_listen")]
        else:
            return []


class CustomActionCheckDomain(Action):
    def name(self) -> Text:
        return "action_check_difficulty"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:   
        difficulty_type=tracker.get_slot("filter_type_difficulty")
        if difficulty_type:
            return [FollowupAction("action_listen")]
        else:
            return []
