import urllib
from urllib import request, error, parse
import json
from pathlib import Path
from .Utils import Utils


class WorldCatAPI:

    PATH = Path(__file__).parent / "data/wskey.conf"

    def __init__(self):
        with open(self.PATH, encoding="utf-8") as f:
            self.__wskeydata = json.load(f)

        self.__URLopensearch = "http://www.worldcat.org/webservices/catalog/search/opensearch?"

    def searchBook(self, keyword):
        url = self.getURL(keyword)

        try:
            uh = urllib.request.urlopen(url)
            content = uh.read()
            return content

        except urllib.error.HTTPError as e:
            return None

    def getURL(self, title):

        type = "kw"

        consulta = {"wskey": self.__wskeydata["key"], "count": 10, "start": 0}
        if type == "kw":
            consulta['q'] = 'srw.kw all "' + title + '"'

        consulta['q'] = consulta['q'] + 'and srw.li all "' + self.__wskeydata["oclc_symbol"]
        consulta['q'] = consulta['q'] + '" and srw.la all "spa"'
        return self.__URLopensearch + urllib.parse.urlencode(consulta)
