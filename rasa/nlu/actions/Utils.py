#coding: utf8
import json
import urllib
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XML, fromstring 


class Utils:
    @staticmethod
    def isEntityInTracker(entity, tracker):

        if len(tracker.latest_message['entities']) <= 0:
            return False

        for track in tracker.latest_message['entities']:
            if entity in track["entity"]:
                return True
        return False

    @staticmethod
    def getValueFromEntity(entity, tracker):
        if len(tracker.latest_message['entities']) <= 0:
            return None

        for track in tracker.latest_message['entities']:
            if entity in track["entity"]:
                return track["value"]
        return None
        
    @staticmethod
    def xmlToArray(xmlResponse):
        # Clean WorldCAT response of newline escaped characters
        xmlResponse = re.sub(r'\n |\n', '', xmlResponse)
        root = ET.fromstring(xmlResponse)

        myArray=[]

        for child in root:
            entryDict = {}
            tagReg = r'{.+}'
            childTag = re.sub(tagReg, '', child.tag)
            if childTag == 'entry':
                for subchild in child:
                    subchildTag = re.sub(tagReg, '', subchild.tag)
                    infoTags = ['title', 'recordIdentifier', 'identifier', 'updated']
                    unavailableText = "{} unavailable"

                    if subchildTag in infoTags:
                        entryDict[subchildTag] = subchild.text if subchild.text != None and len(subchild.text) >= 0 else unavailableText.format(subchildTag.capitalize())
                    
                    elif subchildTag == 'link':
                        entryDict[subchildTag] = subchild.attrib if subchild.attrib != None and len(subchild.attrib) >= 0 else unavailableText.format(subchildTag.capitalize())

                    elif subchildTag == 'author':
                        for nameTag in subchild:
                            subchildNameTag = re.sub(tagReg, '', nameTag.tag)
                            entryDict[subchildNameTag] = nameTag.text if nameTag.text != None and len(nameTag.text) >= 0 else unavailableText.format(subchildNameTag.capitalize())
            
            if len(entryDict) > 0:
                jsonDict = json.dumps(entryDict)
                myArray.append(jsonDict)

        return (str(myArray)) 

    @staticmethod
    def answerBuilder(domain, intentName):
        
        custom_response = domain.get("responses").get("utter_" + intentName)[0].get("custom")
        print('custom_response ', custom_response)
        
        return custom_response