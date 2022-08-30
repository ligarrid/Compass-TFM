# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
import yaml
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType, FollowupAction, AllSlotsReset
from .UtilitiesJSON import UtilitiesJSON as Ujson
from .Utils import Utils
from .InteractorWorldCat import WorldCatAPI
from .ConversationData import ConversationData
from pathlib import Path



class LIBFormAction(Action):

    def name(self) -> Text:
        return "LIB_form"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ConversationData.setSessionData(
            ConversationData(),
            tracker.get_intent_of_latest_message(skip_fallback_intent=False),
            "Library_form",
            tracker.slots)

        print(ConversationData.controlVariable, '\n', 
            ConversationData.previousIntent, '\n', 
            ConversationData.entityList)

        if ConversationData.controlVariable == "Library_form":

            path = Path(__file__).parent / "data/LIBnames.yaml"
            lookupLIB = open(path)
            parsed_yaml_file = yaml.load(lookupLIB, Loader=yaml.FullLoader)

            LIBlist = parsed_yaml_file["nlu"][0]["examples"].split("\n- ")
            
            if tracker.slots.get("LIB_name") is None or tracker.slots.get("LIB_name") not in LIBlist:
                dispatcher.utter_message(response="utter_LIB_form_LIB_name")
            else:

                print("detecta biblio")
                return [FollowupAction("LIB_get_info"), AllSlotsReset()]

        if tracker.slots.get("resource_type") is not None and tracker.slots.get("resource_type") != "biblioteca":
            dispatcher.utter_message(text="te refieres a una biblio?")

        if tracker.slots.get("resource_type") is None:
            template_text = domain.get("responses").get("te refieres a una biblio?")  # TODO: create a response for no type of serach?
            dispatcher.utter_message(text=template_text)
            return []

        return []


class GetLIBInfo(Action):

    def name(self) -> Text:
        return "LIB_get_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tracker.latest_message['text'] = tracker.latest_message['text'].translate(
            {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})

        #print(tracker.slots)

        if Utils.isEntityInTracker("LIB_name", tracker):
            lib = Ujson().getKeyWord(Utils.getValueFromEntity("LIB_name", tracker))

            template_response = domain.get("responses").get("utter_ask_info_LIBR")[0]
            # TODO añadir control cuando NoneType por falta de ortografia (nombre no existe en BDD) done, not tested
            print(template_response)
            template_text = template_response["custom"]['0']['text']
            if lib["name"] is not None:
                template_text = template_text.format(lib["name"],
                                                     lib["open_hour"],
                                                     lib["close_hour"],
                                                     lib["direccion"],
                                                     lib["telefono"],
                                                     lib["email"])
            else:
                # TODO: añadir respuesta catch en la entrada de respuestas nlu
                dispatcher.utter_message(text="Lo siento no puedo encontrar la bibliteca que buscas")

            dispatcher.utter_message(text=template_text)
            ConversationData.resetConversationData(ConversationData())
            print(ConversationData.controlVariable, '\n',
                  ConversationData.previousIntent, '\n',
                  ConversationData.entityList)

        return [AllSlotsReset()]


class BOOKFormAction(Action):

    def name(self) -> Text:
        return "BOOK_form"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # if tracker.slots.get("resource_type") is None:
        #     dispatcher.utter_message(text="te refieres a un libro?")
        #     return []
        # reversed_events = list(reversed(tracker.events))

        ConversationData.setSessionData(
            ConversationData(),
            tracker.get_intent_of_latest_message(skip_fallback_intent=False),
            "Book_form",
            tracker.slots)

        print(ConversationData.controlVariable, '\n', 
            ConversationData.previousIntent, '\n', 
            ConversationData.entityList)


        if tracker.slots.get("resource_type") == "fondo":
            if tracker.slots.get("BOOK_KW") is None:
                dispatcher.utter_message(response="utter_BOOK_form_BOOK_KW")
                
                # list of events "search for event: user" y dentro parse_data.intent.name
                # print(reversed_events)
            elif tracker.slots.get("BOOK_KW") is not None:
                print(tracker.latest_message['entities'])
                return [FollowupAction("BOOK_get_info"), AllSlotsReset()]

            else:
                template_text = domain.get("responses").get("utter_fallback")["text"][0]
                dispatcher.utter_message(text=template_text)
                return []

        elif tracker.slots.get("resource_type") is None and tracker.slots.get("BOOK_KW") is not None:
            tracker.slots["resource_type"] = "fondo"
            print('2' + str(tracker.latest_message['entities']))
            tracker.slots.get("resource_type")
            return [FollowupAction("BOOK_get_info"), AllSlotsReset()]

        return []


class GetBook(Action):
    def name(self) -> Text:
        return "BOOK_get_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # print(tracker.latest_message['entities'])
        tracker.latest_message['text'] = tracker.latest_message['text'].translate(
            {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})


        if Utils.isEntityInTracker("BOOK_KW", tracker):
            xmlString = WorldCatAPI().searchBook(Utils.getValueFromEntity("BOOK_KW", tracker))
            print (xmlString)

            if xmlString is not None:
                xml_message = "{}".format(xmlString)
                xml_message = Utils.xmlToArray(xml_message)

                custom_response = domain.get("responses").get("utter_find_BOOK")[0].get("custom")

                # print('CUSTOM RESPONSE', custom_response)
                domain_text = custom_response['1']['text']
                # print('DOMAIN TEXT', domain_text)
                domain_text = domain_text.format(xml_message)

                custom_response['1']['text'] = domain_text
                dispatcher.utter_message(json_message = custom_response)

            else:
                dispatcher.utter_message(
                    text="La consulta al catálogo ha fallado. Por favor inténtalo en unos minutos.")

        ConversationData.resetConversationData(ConversationData())
        print(ConversationData.controlVariable, '\n',
                ConversationData.previousIntent, '\n',
                ConversationData.entityList)

        return [AllSlotsReset()]


class resetSlots(Action):
    def name(self) -> Text:
        return "ResetSlots"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("hi")

        return [AllSlotsReset()]



class CheckFallbackContext(Action):
    def name(self) -> Text:
        return "check_fallback_context"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if ConversationData.controlVariable == 'Book_form' and ConversationData.previousIntent == "DIA-INT-find_BOOK":
            tracker.slots["BOOK_KW"] = tracker.latest_message['text']
            return [FollowupAction("BOOK_get_info")]
        else:
            template_text = domain.get("responses").get("utter_nlu_fallback")[0].get("text")
            dispatcher.utter_message(text=template_text)


        return []

"""
class NoInfoBook(Action):
    def name(self) -> Text:
        return "BOOK_no_info"

    def run(self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
            ) -> List[Dict[Text, Any]]:
        template_text = domain.get("responses").get("utter_BOOK_KW_input")[0].get("text")
        dispatcher.utter_message(text=template_text)

        return []
"""
