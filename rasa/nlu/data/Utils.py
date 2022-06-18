import urllib
import unidecode

#@TODO: Cambiar nombre de clase por UtlisTracker
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
    def testing():
        title = "chomsky"
        author = "noahm"
        __URLopensearch = "http://www.worldcat.org/webservices/catalog/search/opensearch?"

        type = "kw"

        consulta = {"wskey": "UZHxZYiT35F9kDOsFEm7rR2j9HXASw8kbZjgzxigx25hOr6PHTPQ0wUANf95Hrde5tqhPYzB7D5LuIlg", "count": 10, "start": 0}
        if type == "kw":
            consulta['q'] = 'srw.kw all "' + title + '"'
        elif type == "title":
            consulta['q'] = 'srw.ti all "' + title + '"'
        elif type == "author":
            consulta['q'] = 'srw.au all "' + author + '"'
        elif type == "kw_author":
            consulta['q'] = 'srw.kw all "' + title + '"' + ' and srw.au all "' + author + '"'
        elif type == "title_author":
            consulta['q'] = 'srw.ti all "' + title + '"' + ' and srw.au all "' + author + '"'
        consulta['q'] = consulta['q'] + 'and srw.li all "' + "S9M"
        consulta['q'] = consulta['q'] + '" and srw.la all "spa"'
        URL = __URLopensearch + urllib.parse.urlencode(consulta)

        return URL

    @staticmethod
    def lowerClean(string):
        string = string.lower()
        string = unidecode.unidecode(string)
        string = string.replace("ñ", "n")
        return string