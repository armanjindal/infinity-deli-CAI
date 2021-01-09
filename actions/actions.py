from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

def extractName(slot_value, tracker):
    """ Take in the slot value extracted using slot mapping 'from_text' 
    extracts name, and if cannot find returns None"""
    name_entity = next(tracker.get_latest_entity_values("name"), None)
    PERSON_entity = next(tracker.get_latest_entity_values("PERSON"), None)
    resp_words = slot_value.split()
    print(f"Name: {slot_value}, {name_entity}, {PERSON_entity}, {resp_words}")
    if name_entity:
        return name_entity.capitalize()    
    if PERSON_entity:
        return PERSON_entity.capitalize()
    if len(resp_words) == 1:
        return resp_words[0].capitalize()
    return None

class ValidateFirstTimeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_first_form"

    def validate_userName(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        name = extractName(slot_value, tracker)
        if name:
            return {"userName":name}
        else:
            dispatcher.utter_message(text="Sorry I missed that. Can you _just_ type your first name for me?")
            return {"userName": None}