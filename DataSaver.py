import csv

BASE_LOCATION = 'data/'

class DataSaver:
    filename: str

    def set_file_name(self, filename: str):
        self.filename = filename

    def create_header(self, header_params: list) -> None:
        with open(BASE_LOCATION + self.filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header_params)
            writer.writeheader()

    def save_to_csv(self, data_to_save: dict, save_type: str) -> None:
        with open(BASE_LOCATION + self.filename, save_type, newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data_to_save.keys())
            writer.writerow(data_to_save)