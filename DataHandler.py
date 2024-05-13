from DataImporter import DataImporter
from DataSaver import DataSaver
import time

PARAMS = ['@objectid', 'name', 'yearpublished', 'boardgamecategory', 'minplayers', 'maxplayers', 'age', 'minplaytime', 'maxplaytime', 'description', 'image']
BASE_URL = 'https://api.geekdo.com/xmlapi/boardgame/'

class DataHandler:
    def extract_data(self, offset: int = 0, limit: int = 0) -> None:
        data_importer = DataImporter()

        data_saver = DataSaver()
        data_saver.set_file_name('secondBoardGameDataSet.csv')

        if not offset:
            data_saver.create_header(PARAMS)

        import_count = offset
        data_count = 0
        is_there_more_data = True

        time_start = time.time()

        while (is_there_more_data and limit == 0) or (limit != 0 and import_count < limit):
            data_importer.set_import_destination(BASE_URL + str(import_count + 1))
            data = data_importer.import_with_params(PARAMS)

            if isinstance(data, ImportError):
                is_there_more_data = False
                continue

            import_count += 1

            if not data:
                continue

            data_saver.save_to_csv(data, 'a')
            data_count += 1

            print(f'Saving {import_count} boardgame')

        timeEnd = time.time()
        timeElapsed = timeEnd - time_start

        print(f'Data Extraction complete, took {timeElapsed}s , extracted {import_count} board games')