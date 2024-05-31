from DataImporter import DataImporter
from DataSaver import DataSaver
import time

PARAMS = ['@objectid', 'name', 'yearpublished', 'boardgamepublisher',
          'boardgamecategory', 'boardgamemechanic', 'minplayers', 'maxplayers', 'age',
          'minplaytime', 'maxplaytime', 'boardgameexpansion', 'description', 'image']
BASE_URL = 'https://api.geekdo.com/xmlapi/boardgame/'
API_MAX_SIZE = 99

class DataHandler:
    def extract_data(self, offset: int = 0, limit: int = 0) -> None:
        data_importer = DataImporter()

        data_saver = DataSaver()
        data_saver.set_file_name('test.csv')

        if not offset:
            data_saver.create_header(PARAMS)

        import_count = offset + 1
        data_count = 0
        is_there_more_data = True

        time_start = time.time()

        while (is_there_more_data and limit == 0) or (limit != 0 and import_count <= limit):
            api_url = BASE_URL + str(import_count)
            for i in range(import_count, import_count + API_MAX_SIZE):
                api_url += ',' + str(i)

            data_importer.set_import_destination(api_url)

            try:
                data = data_importer.import_with_params(
                    PARAMS,
                    ['name', 'boardgamepublisher'],
                    ['boardgamecategory', 'boardgameexpansion', 'boardgamemechanic']
                )
            except ImportError:
                print('No more data, could not import')
                is_there_more_data = False
                continue
            except Exception as exception:
                print(exception)
                import_count += API_MAX_SIZE
                continue
            
            import_count += API_MAX_SIZE

            if not data:
                continue

            data_saver.save_to_csv(data, 'a')
            data_count += API_MAX_SIZE

            print(f'Saving {data_count}th boardgame | {import_count} total')

        time_end = time.time()
        time_elapsed = time_end - time_start

        print(f'Data Extraction complete, took {time_elapsed}s , extracted {import_count} board games')