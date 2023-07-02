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

# class ValidateSimplePizzaForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_simple_pizza_form"

#     def validate_pizza_size(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate `pizza_size` value."""

#         if slot_value.lower() not in ALLOWED_PIZZA_SIZES:
#             dispatcher.utter_message(text=f"We only accept pizza sizes: s/m/l/xl.")
#             return {"pizza_size": None}
#         dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
#         return {"pizza_size": slot_value}
    
#     def validate_pizza_type(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate `pizza_type` value."""

#         if slot_value not in ALLOWED_PIZZA_TYPES:
#             dispatcher.utter_message(text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}.")
#             return {"pizza_type": None}
#         dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
#         return {"pizza_type": slot_value}

#     def validate_name(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         dispatcher.utter_message(text=f"Hello {slot_value} ")
#         return {"name": slot_value}


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

        
