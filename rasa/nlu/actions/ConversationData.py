
class ConversationData:
    senderID = None
    previousIntent = None
    controlVariable = None
    entityList = None
    searchText = None

    # resource_type y LIB_name
    # value['resource_type']

    def __init__(self, senderID, previousIntent, controlVariable, entityList):
        self.senderID = senderID
        self.previousIntent = previousIntent
        self.controlVariable = controlVariable
        self.searchText = None
        self.entityList = []
        
        self.entityList.append(entityList["LIB_name"])
        self.entityList.append(entityList["resource_type"])
        

    def getSenderID(self):
        return self.senderID

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

        self.entityList.append(value["resource_type"])
        self.entityList.append(value["LIB_name"])
    
    def setEntityList(self, list):
        self.entityList = []
        self.entityList = list

    def setSessionData(self, currentIntent, controlVariable, entityList):
        print("fff")
        # ConversationData.previousIntent = currentIntent
        # ConversationData.controlVariable = controlVariable
        # for entity in entityList:
        #     ConversationData.entityList.append(entityList[entity])

    def resetConversationData(self):
        print("fff")
        # ConversationData.previousIntent = None
        # ConversationData.controlVariable = None
        # ConversationData.searchText = None
        # ConversationData.entityList = []

    def clearConversationData(self):
        self.previousIntent = None
        self.controlVariable = None
        self.searchText = None
        self.entityList = []
