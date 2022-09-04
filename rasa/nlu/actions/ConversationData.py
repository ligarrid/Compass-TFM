
class ConversationData:
    previousIntent = None
    controlVariable = None
    entityList = None
    searchText = None


                #     conversationData = ConversationData(
                #     tracker.get_intent_of_latest_message(skip_fallback_intent=False),
                #     "Library_form",
                #     tracker.slots
                # )

    def __init__(self, previousIntent, controlVariable, entityList):
        self.previousIntent = previousIntent
        self.controlVariable = controlVariable
        self.searchText = None
        self.entityList = entityList


    def getControlVariable(self):
        return self.controlVariable

    def getPreviousIntent(self):
        return self.previousIntent
    
    def getSearchText(self):
        return self.searchText

    def getEntityList(self):
        return self.entityList

    def setSearchText(self, value):
        self.searchText = value

    def setPreviousIntent(self, value):
        self.previousIntent = value

    def setControlVariable(self, value):
        self.controlVariable = value

    def addEntityListItem(self, value):
        self.entityList.append(value)

    def setSessionData(self, currentIntent, controlVariable, entityList):
        ConversationData.previousIntent = currentIntent
        ConversationData.controlVariable = controlVariable
        for entity in entityList:
            ConversationData.entityList.append(entityList[entity])

    def resetConversationData(self):
        ConversationData.previousIntent = None
        ConversationData.controlVariable = None
        ConversationData.searchText = None
        ConversationData.entityList = []
