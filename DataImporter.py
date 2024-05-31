import xmltodict
import requests

BASE_PARAM = 'boardgames'
BOARDGAME_PARAM = 'boardgame'

class DataImporter:
    url: str

    def set_import_destination(self, url: str) -> None:
        self.url = url

    def import_with_params(self, params: list, singular_params: list, multi_key_params: list) -> list | None | ImportError:
        response = requests.get(self.url)

        if response.status_code != 200:
            raise ImportError

        xml_response = response.text
        dict_response = xmltodict.parse(xml_response)

        board_games_dict = dict_response[BASE_PARAM][BOARDGAME_PARAM]

        board_game_dict_list = []

        for board_game_dict in board_games_dict:
            if 'error' in board_game_dict.keys():
                return None

            if len(board_game_dict.keys()) == 0:
                return None

            param_dict = dict.fromkeys(params, '')

            for param in params:
                if param in board_game_dict:
                    param_dict[param] = board_game_dict[param]

            for singular_param in singular_params:
                if singular_param in param_dict.keys() and param_dict[singular_param] != '':
                    param_dict[singular_param] = self.extract_name(param_dict[singular_param])

            for multi_key_param in multi_key_params:
                if multi_key_param in param_dict.keys() and param_dict[multi_key_param] != '':
                    param_dict[multi_key_param] = self.extract_from_list(param_dict[multi_key_param])

            board_game_dict_list.append(param_dict)

        return board_game_dict_list
    
    def extract_name(self, board_game_names: list | dict) -> str:
        if isinstance(board_game_names, list):
            if '#text' in board_game_names[0].keys():
                return(board_game_names[0]['#text'])
            else:
                for board_game_name in board_game_names:
                    if '#text' in board_game_name.keys():
                        return board_game_name['#text']
        else:
            return(board_game_names['#text'])
        
    def extract_from_list(self, board_game_key_list: list | dict) -> list:
        extracted_keys = []

        if isinstance(board_game_key_list, list):
            for key_element in board_game_key_list:
                clean_key_element = self.clean_string(key_element['#text'])
                extracted_keys.append(clean_key_element)
        else:
            clean_key_element = self.clean_string(board_game_key_list['#text'])
            extracted_keys.append(clean_key_element)

        return extracted_keys
    
    def clean_string(self, extracted_string: str) -> str:
        extracted_string = extracted_string.strip()
        extracted_string = extracted_string.strip('"')
        extracted_string = extracted_string.strip("'")
        extracted_string = extracted_string.replace("'", '')
        extracted_string = extracted_string.replace('"', '')
        extracted_string

        return extracted_string