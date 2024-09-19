import csv
import os
import re


class CsvHelper:
    max_lines_per_file = 900

    def __init__(self, file_path):
        self.file_path = file_path
        

    def get_new_file_name(self, counter: int, current_file: str):
        if counter < self.max_lines_per_file:
            return current_file
        elif counter % self.max_lines_per_file == 0:
            file_number = int(counter / self.max_lines_per_file) + 1
            repl = f"_{file_number}.csv"
            pattern1 = "_\d+.csv"
            pattern2 = ".csv"
            what_find = pattern2
            match = re.search(pattern1, current_file)
            if match:
                what_find = pattern1
            return re.sub(what_find, repl, current_file)
        else:
            return current_file


    def write_guests_to_csv(self, guests, csv_file):
        counter = 0
        current_file = csv_file
        for guest in guests:
            row = guest.get_row()
            if row:
                CsvHelper.write_str(row, current_file)
                counter += 1
                new_file = self.get_new_file_name(counter, current_file)
                current_file = new_file
        return current_file


    def read_csv(self):
        """Считывает CSV-файл и возвращает список словарей."""
        data = []
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print(f"Файл {self.file_path} не найден.")
        except Exception as e:
            print(f"Ошибка при чтении CSV-файла: {e}")
        return data


    def write_csv(self, data, fieldnames):
        """Записывает данные в CSV-файл.
        Аргументы:
        - data: список словарей с данными для записи.
        - fieldnames: список названий полей для CSV-файла.
        """
        try:
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f"Ошибка при записи в CSV-файл: {e}")


    def append_csv(self, data, fieldnames):
        """Добавляет данные в существующий CSV-файл."""
        try:
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerows(data)
        except Exception as e:
            print(f"Ошибка при добавлении в CSV-файл: {e}")


    def write_str(row: str, csv_file):
        mode = "a"
        if(not os.path.exists(csv_file)):
            mode = "w"
        with open(csv_file, mode) as csvfile:
                csvfile.write(row)

