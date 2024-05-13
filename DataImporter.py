import xmltodict
import requests
import pprint

BASE_PARAM = 'boardgames'
BOARDGAME_PARAM = 'boardgame'

class DataImporter:
    url: str

    def set_import_destination(self, url: str) -> None:
        self.url = url

    def import_with_params(self, params: list) -> dict | None | ImportError:
        response = requests.get(self.url)

        if response.status_code != 200:
            return ImportError

        xml_response = response.text
        dict_response = xmltodict.parse(xml_response)
        board_game_dict = dict_response[BASE_PARAM][BOARDGAME_PARAM]

        if 'error' in board_game_dict.keys():
            return None

        if len(board_game_dict.keys()) == 0:
            return None

        param_dict = dict.fromkeys(params, '')

        for param in params:
            if param in board_game_dict:
                param_dict[param] = board_game_dict[param]

        if 'name' in param_dict.keys():
            param_dict['name'] = self.extract_name(param_dict['name'])

        if 'boardgamecategory' in param_dict.keys() and param_dict['boardgamecategory'] != '':
            param_dict['boardgamecategory'] = self.extract_category(param_dict['boardgamecategory'])

        return param_dict
    
    def extract_name(self, boardGameNames: list | dict) -> str:
        if isinstance(boardGameNames, list):
            if '#text' in boardGameNames[0].keys():
                return(boardGameNames[0]['#text'])
            else:
                for boardGameName in boardGameNames:
                    if '#text' in boardGameName.keys():
                        return boardGameName['#text']
        else:
            return(boardGameNames['#text'])
        
    def extract_category(self, board_game_categories: list | dict) -> list:
        categories = []

        if isinstance(board_game_categories, list):
            for category in board_game_categories:
                categories.append(category['#text'])
        else:
            categories.append(board_game_categories['#text'])

        return categories