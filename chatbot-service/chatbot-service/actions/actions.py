# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from typing import Text, List, Any, Dict
from rasa_sdk.events import SlotSet, UserUtteranceReverted

class ActionPushMenu(Action):
    """Push the current menu to the menu stack."""
    
    def name(self) -> Text:
        return "action_push_menu"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        menu_stack = tracker.get_slot("menu_stack") or []
        current_intent = tracker.latest_message.get("intent", {}).get("name")
        user_message = tracker.latest_message.get("text", "")
        
        is_arabic = any("\u0600" <= char <= "\u06FF" for char in user_message)
        main_menu = "main_menu_ar" if is_arabic else "main_menu_en"
        
        if current_intent:
            if current_intent in ["main_menu_ar", "main_menu_en"]:
                menu_stack = [current_intent]
            elif current_intent == "nlu_fallback":
                menu_stack.append(main_menu)
            elif not menu_stack or menu_stack[-1] != current_intent:
                menu_stack.append(current_intent)
        
        return [SlotSet("menu_stack", menu_stack)]

class ActionPopMenu(Action):
    def name(self) -> Text:
        return "action_pop_menu"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        menu_stack = tracker.get_slot("menu_stack") or []
        user_message = tracker.latest_message.get("text", "")
        is_arabic = (any("\u0600" <= char <= "\u06FF" for char in user_message) or user_message.endswith("_ar"))
        main_menu = "utter_main_menu_ar" if is_arabic else "utter_main_menu_en"
        previous_menu = menu_stack.pop() if menu_stack else None
        previous_menu = menu_stack[-1] if menu_stack else None
        
        if previous_menu==("welcome"):
            dispatcher.utter_message(response="utter_main_menu_ar")
        elif previous_menu==("welcome_en"):
            dispatcher.utter_message(response="utter_main_menu_en")
        elif previous_menu:
            dispatcher.utter_message(response=f"utter_{previous_menu}")
        else:
            dispatcher.utter_message(response=main_menu)

        return [SlotSet("menu_stack", menu_stack)]
    
class ActionCustomFallback(Action):
    def name(self):
        return "action_custom_fallback"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "")

        if any("\u0600" <= char <= "\u06FF" for char in user_message):
            dispatcher.utter_message(response="utter_default_message")
            dispatcher.utter_message(response="utter_main_menu_ar")
        else:
            dispatcher.utter_message(response="utter_default_message_en")
            dispatcher.utter_message(response="utter_main_menu_en")
        return []