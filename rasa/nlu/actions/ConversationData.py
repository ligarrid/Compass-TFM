

class ConversationData:
    previousIntent = None
    controlVariable = None
    entityList = []
    searchText = None

    def __init__(self):
        self.previousIntent = None
        self.controlVariable = None
        self.searchText = None
        self.entityList = []

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
