# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
import yaml
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, AllSlotsReset
from .UtilitiesJSON import UtilitiesJSON as Ujson
from .Utils import Utils
from .InteractorWorldCat import WorldCatAPI
from .ConversationData import ConversationData
from pathlib import Path


class SingletonClass(object):
    conversationsData = []
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance

    def getConversationsData(self, id):
        for conversationData in self.conversationsData:
            if conversationData.getSenderID() == id:
                return conversationData

        return None

    def appendConversationsData(self, data):
        self.conversationsData.append(data)


class LIBFormAction(Action):

    def name(self) -> Text:
        return "LIB_form"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print('INIT LIBFormAction')

        singleton = SingletonClass()
        conversationData = singleton.getConversationsData(tracker.sender_id)

        if conversationData is not None:
            conversationData.setPreviousIntent(tracker.get_intent_of_latest_message(skip_fallback_intent=False))
            conversationData.setControlVariable("Library_form")
            conversationData.addEntityListItem(tracker.slots)
        else:
            conversationData = ConversationData(
                tracker.sender_id,
                tracker.get_intent_of_latest_message(skip_fallback_intent=False),
                "Library_form",
                tracker.slots
            )
            singleton.appendConversationsData(conversationData)


        if conversationData.getControlVariable() == "Library_form":
            
            path = Path(__file__).parent / "data/LIBnames.yaml"
            lookupLIB = open(path)
            parsed_yaml_file = yaml.load(lookupLIB, Loader=yaml.FullLoader)

            LIBlist = parsed_yaml_file["nlu"][0]["examples"].split("\n- ")

            conversationData.setEntityList([tracker.slots.get("LIB_name")])

            if tracker.slots.get("LIB_name") is not None and tracker.slots.get("LIB_name").lower() in LIBlist:

                print('INFO LIBFormAction: LIB_NAME detected ', tracker.slots.get("LIB_name"))
                
                # conversationData.setEntityList([tracker.slots.get("LIB_name")])
                print("getEntityList(): ", conversationData.getEntityList())
                print('ENDED LIBFormAction: library found')
                return [FollowupAction("LIB_get_info"), AllSlotsReset()]

            else:

                dispatcher.utter_message(json_message = Utils.answerBuilder(domain, intentName='LIB_form_LIB_name'))
                print('ENDED LIBFormAction: no library name')
                       

        return []


class GetLIBInfo(Action):

    def name(self) -> Text:
        return "LIB_get_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('INIT GetLIBInfo')
        
        tracker.latest_message['text'] = tracker.latest_message['text'].translate(
            {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})


        singleton = SingletonClass()
        conversationData = singleton.getConversationsData(tracker.sender_id)

        if len(conversationData.getEntityList()) > 0:
            lib = Ujson().getKeyWord(conversationData.getEntityList()[0])
            print("getEntityList(): ", conversationData.getEntityList())
            print("LIB: ", lib)

            custom_response = domain.get("responses").get("utter_ask_info_LIBR")[0].get("custom")

            template_text = custom_response['0']['text']
            if lib["name"] is not None:
                template_text = template_text.format(lib["name"],
                                                     lib["open_hour"],
                                                     lib["close_hour"],
                                                     lib["direccion"],
                                                     lib["telefono"],
                                                     lib["email"])
                custom_response['0']['text'] =  template_text                                    
                dispatcher.utter_message(json_message = custom_response)
                print('INFO GetLIBInfo: library info returned')
            else:
                
                dispatcher.utter_message(json_message = Utils.answerBuilder(domain, intentName='found_noLIB'))
                print('INFO GetLIBInfo: no library result')

            conversationData.clearConversationData()

        print('ENDED GetLIBInfo')
        return [AllSlotsReset()]


class BOOKFormAction(Action):

    def name(self) -> Text:
        return "BOOK_form"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('INIT BOOKFormAction')

        singleton = SingletonClass()
        conversationData = singleton.getConversationsData(tracker.sender_id)

        if conversationData is not None:
            conversationData.setPreviousIntent(tracker.get_intent_of_latest_message(skip_fallback_intent=False))
            conversationData.setControlVariable("Book_form")
            conversationData.addEntityListItem(tracker.slots)
        else:
            conversationData = ConversationData(
                tracker.sender_id,
                tracker.get_intent_of_latest_message(skip_fallback_intent=False),
                "Book_form",
                tracker.slots
            )
            singleton.appendConversationsData(conversationData)

        if tracker.slots.get("resource_type") == "fondo":

            if conversationData.getSearchText() is None:
                print('INFO BOOKFormAction: controlVariable ', conversationData.getControlVariable())
                print('INFO BOOKFormAction: searchText None', conversationData.getSearchText())
                print('ENDED BOOKFormAction: no search text found')
                dispatcher.utter_message(json_message = Utils.answerBuilder(domain, intentName='BOOK_form_BOOK_KW'))

                return []

            elif conversationData.getSearchText() is not None:
                print('INFO BOOKFormAction: controlVariable ', conversationData.getControlVariable())
                print('INFO BOOKFormAction: searchText not None ', conversationData.getSearchText())
                print('ENDED BOOKFormAction: send search to catalogue')
                
                return [FollowupAction("BOOK_get_info"), AllSlotsReset()]

            # Added as security filter, this should never happen
            else:
                dispatcher.utter_message(json_message = Utils.answerBuilder(domain, intentName='nlu_fallback'))
                print('ENDED BOOKFormAction: fallback')
                
                return []
        
        # Added as security filter, this should never happen
        elif tracker.slots.get("resource_type") is None and conversationData.getSearchText() is not None:
            tracker.slots["resource_type"] = "fondo"
            print('ENDED BOOKFormAction: forced query')
            return [FollowupAction("BOOK_get_info"), AllSlotsReset()]
        
        print('ENDED BOOKFormAction')
        return []


class GetBook(Action):
    def name(self) -> Text:
        return "BOOK_get_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('INIT BOOK_get_info')

        # recommended way (by Rasa) to handle special chars in user input
        tracker.latest_message['text'] = tracker.latest_message['text'].translate(
            {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})

        singleton = SingletonClass()
        conversationData = singleton.getConversationsData(tracker.sender_id)

        if conversationData.getSearchText() is not None:
            xmlString = WorldCatAPI().searchBook(conversationData.getSearchText())
            print (xmlString)

            if xmlString is not None:
                xml_message = "{}".format(xmlString)
                # @TODO: manejo de acentuación latina y demás chars
                xml_message = Utils.xmlToArray(xml_message)

                custom_response = domain.get("responses").get("utter_find_BOOK")[0].get("custom")
                
                domain_text = custom_response['1']['text']
                domain_text = domain_text.format(xml_message)
                
                custom_response['1']['text'] = str(domain_text)
                print('INFO BOOK_get_info: custom_response ', custom_response)

                dispatcher.utter_message(json_message=custom_response)
                conversationData.clearConversationData()

                print('ENDED BOOK_get_info: successful query')
                return [AllSlotsReset()]

            else:
                
                dispatcher.utter_message(json_message = Utils.answerBuilder(domain, intentName='BOOK_form_CatError'))
                conversationData.clearConversationData()

                print('ENDED BOOK_get_info: no query to make')
                return [AllSlotsReset()]

        return []

class resetSlots(Action):
    def name(self) -> Text:
        return "ResetSlots"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('INIT ResetSlots')

        singleton = SingletonClass()
        conversationData = singleton.getConversationsData(tracker.sender_id)

        conversationData.clearConversationData()
        print('ENDED ResetSlots')
        return [AllSlotsReset()]



class CheckFallbackContext(Action):
    def name(self) -> Text:
        return "check_context"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('INIT check_context')
        last_intent = tracker.get_intent_of_latest_message(skip_fallback_intent=False)

        print(tracker.sender_id)

        singleton = SingletonClass()
        conversationData = singleton.getConversationsData(tracker.sender_id)
        

        if conversationData is None: ## Aqui entra cuando no tienes conversacion guardada
            conversationData = ConversationData(
                tracker.sender_id,
                tracker.get_intent_of_latest_message(skip_fallback_intent=False),
                None,
                tracker.slots
            )
            singleton.appendConversationsData(conversationData)
            dispatcher.utter_message(json_message = Utils.answerBuilder(domain, last_intent))
            return []
        else:
            print("CONTROL VAR: ", conversationData.getControlVariable())
            # Segunda vez que entramos a formulario de consulta de libros
            if conversationData.getControlVariable() == "Book_form":
                print("pruebasCarlos", 'INFO check_context: Book_form parameter detected')
                conversationData.setSearchText(tracker.latest_message['text'])
                print("pruebasCarlos", 'ENDED check_context')
                return [FollowupAction("BOOK_form")]
            else:
                print('INFO check_context: Book_form parameter NOT detected')

                non_query_intents = ['CHI-greetings', 'CHI-negative', 'CHI-affirmative', 'CHI-thankyou', 'CHI-hate', 'CHI-startOver', 'CHI-botIdentity', 'CHI-help', 'CHI-talkToHuman', 'CHI-stop']
                if last_intent in non_query_intents:

                    print('INFO check_context: non-query intent ', last_intent)
                    dispatcher.utter_message(json_message = Utils.answerBuilder(domain, last_intent))
                
                # Primera vez que entramos a formulario de consulta de libros
                elif last_intent == 'DIA-INT-find_BOOK':
                    print('ENDED check_context: form intent ', last_intent)
                    return [FollowupAction("BOOK_form")]

                elif last_intent == 'DIA-INT-ask_info_LIBR':
                    print('ENDED check_context: form intent ', last_intent)
                    return [FollowupAction("LIB_form")]

                # else for fallback intent
                else:
                    print('INFO check_context: INTENT ', last_intent)
                    dispatcher.utter_message(json_message = Utils.answerBuilder(domain, last_intent))

        print('ENDED check_context')
        return []


    

