import csv

BASE_LOCATION = 'data/'

class DataSaver:
    fileName: str

    def setFileName(self, fileName: str):
        self.fileName = fileName

    def createHeader(self, headerParams: list) -> None:
        with open(BASE_LOCATION + self.fileName, 'w', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=headerParams)
            writer.writeheader()

    def saveToCsv(self, dataToSave: dict, saveType: str) -> None:
        with open(BASE_LOCATION + self.fileName, saveType, newline='', encoding='utf-8') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=dataToSave.keys())
            writer.writerow(dataToSave)