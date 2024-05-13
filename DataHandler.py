from DataImporter import DataImporter
from DataSaver import DataSaver
import time

PARAMS = ['@objectid', 'name', 'yearpublished', 'boardgamecategory', 'minplayers', 'maxplayers', 'age', 'minplaytime', 'maxplaytime', 'description', 'image']
BASE_URL = 'https://api.geekdo.com/xmlapi/boardgame/'

class DataHandler:
    def extractData(self, offset: int = 0, limit: int = 0) -> None:
        dataImporter = DataImporter()

        dataSaver = DataSaver()
        dataSaver.setFileName('secondBoardGameDataSet.csv')

        if not offset:
            dataSaver.createHeader(PARAMS)

        importCount = offset
        dataCount = 0
        isThereMoreData = True

        timeStart = time.time()

        while (isThereMoreData and limit == 0) or (limit != 0 and importCount < limit):
            dataImporter.setImportDestination(BASE_URL + str(importCount + 1))
            data = dataImporter.importWithParams(PARAMS)

            if isinstance(data, ImportError):
                isThereMoreData = False
                continue

            importCount += 1

            if not data:
                continue

            dataSaver.saveToCsv(data, 'a')
            dataCount += 1

            print(f'Saving {importCount} boardgame')

        timeEnd = time.time()
        timeElapsed = timeEnd - timeStart

        print(f'Data Extraction complete, took {timeElapsed}s , extracted {importCount} board games')