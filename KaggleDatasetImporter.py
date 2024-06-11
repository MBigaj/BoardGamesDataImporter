from zipfile import ZipFile
import os

DATA_DIRECTORY = 'data/'
DATASET_URL = 'mikoajbigaj/bgg-board-game-dataset'
DATASET_ZIP = 'bgg-board-game-dataset.zip'


class KaggleDatasetImporter:
    @staticmethod
    def import_from_kaggle() -> None:
        if not os.path.exists(DATA_DIRECTORY):
            os.mkdir(DATA_DIRECTORY)

        os.system(f'kaggle datasets download -d {DATASET_URL}')

        with ZipFile(DATASET_ZIP, 'r') as zip_file:
            zip_file.extractall(DATA_DIRECTORY)

        os.remove(DATASET_ZIP)