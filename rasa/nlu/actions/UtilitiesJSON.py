import json
import unidecode


class UtilitiesJSON:
    PATH = "D:/Desktop/pruebas-rasa-webchat/rasa/nlu/data/LIBdata.json"
    jsonData = ""

    def __init__(self):
        # body of the constructor
        f = open(self.PATH, encoding="utf8")

        # returns JSON object as
        # a dictionary
        self.jsonData = json.load(f)
        f.close()

    def getKeyWord(self, keyword):
        for data in self.jsonData:
            for kw in data["kw"]:
                unaccented_keyword = unidecode.unidecode(keyword)
                unaccented_kw = unidecode.unidecode(kw)
                if unaccented_keyword.lower() in unaccented_kw.lower():
                    return data
        return None
