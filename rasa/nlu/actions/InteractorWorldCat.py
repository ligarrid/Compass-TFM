import urllib
from urllib import  error, parse
from urllib.request import Request, urlopen
import json
from pathlib import Path
from .Utils import Utils
import http.client
import requests

class WorldCatAPI:

    PATH = Path(__file__).parent / "data/wskey.conf"

    def __init__(self):
        with open(self.PATH, encoding="utf-8") as f:
            self.__wskeydata = json.load(f)

        self.__URLopensearch = "http://www.worldcat.org/webservices/catalog/search/opensearch?"

    def searchBook(self, keyword):
        url = self.getURL(keyword)

        try:
            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            return response.text

        except urllib.error.HTTPError as e:
            return e

    def getURL(self, title):

        type = "kw"

        consulta = {"wskey": self.__wskeydata["key"], "count": 5, "start": 0}
        if type == "kw":
            consulta['q'] = 'srw.kw all "' + title + '"'

        consulta['q'] = consulta['q'] + 'and srw.li all "' + self.__wskeydata["oclc_symbol"]
        consulta['q'] = consulta['q'] + '" and srw.la all "spa"'
        return self.__URLopensearch + urllib.parse.urlencode(consulta)




