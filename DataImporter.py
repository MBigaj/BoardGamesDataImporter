import xmltodict
import requests
import pprint

BASE_PARAM = 'boardgames'
BOARDGAME_PARAM = 'boardgame'

class DataImporter:
    url: str

    def setImportDestination(self, url: str) -> None:
        self.url = url

    def importWithParams(self, params: list) -> dict | None | ImportError:
        response = requests.get(self.url)

        if response.status_code != 200:
            return ImportError

        xmlResponse = response.text
        dictResponse = xmltodict.parse(xmlResponse)
        boardGameDict = dictResponse[BASE_PARAM][BOARDGAME_PARAM]

        if 'error' in boardGameDict.keys():
            return None

        if len(boardGameDict.keys()) == 0:
            return None

        paramDict = dict.fromkeys(params, '')

        for param in params:
            if param in boardGameDict:
                paramDict[param] = boardGameDict[param]

        if 'name' in paramDict.keys():
            paramDict['name'] = self.extractName(paramDict['name'])

        if 'boardgamecategory' in paramDict.keys() and paramDict['boardgamecategory'] != '':
            paramDict['boardgamecategory'] = self.extractCategory(paramDict['boardgamecategory'])

        return paramDict
    
    def extractName(self, boardGameNames: list | dict) -> str:
        if isinstance(boardGameNames, list):
            if '#text' in boardGameNames[0].keys():
                return(boardGameNames[0]['#text'])
            else:
                for boardGameName in boardGameNames:
                    if '#text' in boardGameName.keys():
                        return boardGameName['#text']
        else:
            return(boardGameNames['#text'])
        
    def extractCategory(self, boardGameCategories: list | dict) -> list:
        categories = []

        if isinstance(boardGameCategories, list):
            for category in boardGameCategories:
                categories.append(category['#text'])
        else:
            categories.append(boardGameCategories['#text'])

        return categories