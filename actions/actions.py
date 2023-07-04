import string
import random
import pandas as pd
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
insurance_ids = [
    'ABC1234',
    'XYZ5678',
    'DEF9012',
    'GHI3456',
    'JKL7890',
    'MNO2345',
    'PQR6789',
    'STU0123',
    'VWX4567',
    'YZA8901',
    'BCD2345',
    'EFG6789',
    'HIJ0123',
    'KLM4567',
    'NOP8901',
    'QRS2345',
    'TUV6789', 
    'WXY0123',
    'ZAB4567',
    'CDE8901'
]
claim_ids = [
    'AB12345',
    'CD67890',
    'EF23456',
    'GH78901',
    'IJ34567',
    'KL89012',
    'MN45678',
    'OP90123',
    'QR56789',
    'ST01234',
    'UV67890',
    'WX23456',
    'YZ78901',
    'AB34567',
    'CD89012',
    'EF45678',
    'GH90123',
    'IJ56789',
    'KL01234',
    'MN67890'
]

CLAIMS = [  ['XX123456', 20201004, 0, 'Final'],
            ['AB234567', 20200312, 5000, 'Pending'],
            ['Z345678', 20201130, 200, 'Submitted'],
            ['C456789', 20200903, 500, 'Final'],
            ['CL567890', 20200203, 3000, 'Pending']
]

QUOTE_CLAIM=[
    ["health",250],
    ["vehicle",50],
    ["life",150],
    ["home",200]
]

CLIENTS=[
    ["USER1","kushal","IIITB,Street No. 17","Bangalore","Karnataka","12345"]
]
class ActionInit(Action):
    def name(self) -> Text:
        return "action_init"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # amounts = [random.randint(1, 50000) for _ in range(20)]
        # df=pd.DataFrame(columns=["insurance_ids", "claim_ids"])
        # for i in range(20):
        #     new_row = {'insurance_ids': insurance_ids[i], 'claim_ids': claim_ids[i]}
        #     df.loc[len(df)] = new_row
        # df.to_csv("data.csv",index=False)
        # df1=pd.DataFrame(columns=["claim_ids","amounts"])
        # for i in range(20):
        #     new_row = {'claim_ids': claim_ids[i], 'amounts':amounts[i]}
        #     df1.loc[len(df1)] = new_row
        # df1.to_csv('claims.csv',index=False)
        return []

class ActionFileAClaim(Action):
    def name(self) -> Text:
        return "action_file_claim"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        insurance_id = tracker.get_slot("insurance_id")
        bill_amount = tracker.get_slot("bill_amount")
        letters = random.choices(string.ascii_uppercase, k=2)
        numbers = random.choices(string.digits, k=5)
        res = ''.join(letters) + ''.join(numbers)
        new_row = {'insurance_ids': insurance_id, 'claim_ids': res}
        df=pd.read_csv("data.csv")
        # df['insurance_ids']=df['insurance_ids'].append(insurance_id)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv('data.csv',index=False)
        new_row1 = {'claim_ids': res, 'amounts': bill_amount}
        df2=pd.read_csv("claims.csv")
        df2 = pd.concat([df2, pd.DataFrame([new_row1])], ignore_index=True)
        df2.to_csv('claims.csv', index=False)
        dispatcher.utter_message(f"Your claim for Insurance {res} has been submitted. Please note claim ID {res} for future reference.")
        return []

class ValidateUserRegisterForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_register_form"

    def validate_gender(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value.lower() == 'male' or slot_value.lower() == 'm':
            return {"gender": 'm'}
        elif slot_value.lower() == 'female' or slot_value.lower()=='f':
            return {"gender": 'f'}
        elif slot_value.lower() == 'other':
            return {"gender": 'other'}
        else:
            dispatcher.utter_message(text=f"Please write the correct gender among m/f/other.")
            return {"gender": None}
        
class ActionRegisterUser(Action):
    def name(self) -> Text:
        return "action_register_user"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        
        letters = random.choices(string.ascii_uppercase, k=5)
        numbers = random.choices(string.digits, k=5)
        res = ''.join(letters) + ''.join(numbers)
        location = tracker.get_slot("location")
        age = tracker.get_slot("age")
        occupation = tracker.get_slot("occupation")
        monthly_income = tracker.get_slot("monthly_income")
        gender = tracker.get_slot("gender")
        user_id=res
        dispatcher.utter_message(f"Your user Id is {res}.Thank for registering.")


class ActionCheckClaimStatus(Action):

    def name(self) -> Text:
        return "action_check_claim_status"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        user_clm_id = tracker.get_slot("claim_id")
        claim=False
        claimStatus=""
        for i in CLAIMS:
            if (str(i[0])==user_clm_id):
                claim=True
                claimStatus=str(i[3])
                break                
        if (claim == False):
            dispatcher.utter_message("Please enter the correct Claim-ID")
            return [SlotSet("claim_id", None)]
        else:
            dispatcher.utter_message(f"The claim status is {claimStatus}")
            return [SlotSet("claim_id", None)]



class ActionGetQuote(Action):

    def name(self) -> Text:
        return "action_quote_form"
    
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        # slots = ["insurance_type", "number_of_persons","state"]
        insurance_type=tracker.get_slot("insurance_type")
        n_persons = int(tracker.get_slot("number_of_persons"))
        quote_state=tracker.get_slot("state")
        base=0
        for i in QUOTE_CLAIM:
            if (i[0]==insurance_type):
                base=i[1]
        final_quote=base*n_persons
        dispatcher.utter_message(f"Your monthly payment given the information provided is: {final_quote} per month Insurance Type: {insurance_type} Policy State: {quote_state} Number of people on policy: {n_persons}")

        # return [SlotSet(slot, None) for slot in slots]
        return []

class ValidateUserForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_user_id_form"
    
    def validate_user_id(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        user_id = tracker.get_slot("user_id")
        name=""
        street=""
        city=""
        state=""
        pincode=""
        for i in CLIENTS:
            if (i[0]== user_id):
                name = i[1]
                street = i[2]
                city = i[3]
                state = i[4]
                pincode = i[5]
        
        full_address=f"{street},{city},{state},{pincode}"

        dispatcher.utter_message(f"Please confirm the address {name}: {full_address}")

        return {user_id : user_id}
class ActionGoodbye(Action):
    def name(self) -> Text:
        return "action_goodbye"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        slots = ["insurance_type","number_of_persons","state",]
        return [SlotSet(slot, None) for slot in slots]
        return []
        
































# 