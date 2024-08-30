import json
import csv
import os
import re
from openpyxl import Workbook


def main():
    current_dir = os.path.dirname(__file__)
    in_dir = os.path.join(current_dir, "in")
    json_files = list_files_in_directory(in_dir)
    dictionary = get_dictionary(os.path.join(current_dir, "dict.csv"))
    for file in json_files:
        if get_file_extension(file) == '.txt' or get_file_extension(file) == '.json':
            with open(file, 'r', encoding='utf8') as json_file:
                try:
                    data = json.load(json_file)
                except Exception as ex:
                    input(f'Ошибка при попытке загрузки json-данных из файла {file}: {ex}')
                    return
            flattened_data = flatten_json_list(data)
            excel_file = file.replace("in", "out").replace(get_file_extension(file), '.xlsx')
            json_to_excel(flattened_data, excel_file, dictionary)
            print(f'Данные успешно записаны в {excel_file}')

def get_dictionary(dict_file: str):
    lines = read_lines_from_file(dict_file)
    data_dict = {}
    for line in lines:
        arr = line.split(";")
        key = arr[0]
        value = arr[1]
        if key is not None and value is not None:
            data_dict[key] = value
    return data_dict

def read_lines_from_file(file_path):
    lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
    return lines

def flatten_json(data):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for key in x:
                flatten(x[key], name + key + '.')
        elif isinstance(x, list):
            for item in x:
                flatten(item, f'{name}')
        else:
            if "Dttm" in name:
                x = iso_date_normalize(x)
            out[name[:-1]] = x
    flatten(data)
    return out

def flatten_json_list(json_list):
    return [flatten_json(item) for item in json_list]

def iso_date_normalize(iso_date):
    return str(iso_date).replace('T', ' ').replace('Z', '')

def is_iso_date(str: str) -> bool:
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    match = re.match(pattern, str)
    return match is not None

def json_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        if isinstance(data, list) and len(data) > 0:
            fieldnames = get_headers(data)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

def json_to_excel(data: list[dict], excel_file: str, dictionary: dict):
    wb = Workbook()
    ws = wb.active
    if isinstance(data, list) and len(data) > 0:
        headers = get_headers(data)
        ws.append(headers)
        for row in data:
            r = [get_value(header, row, dictionary) for header in headers]
            ws.append(r)
    wb.save(excel_file)

def get_value(header, row, dictionary):
    value = row.get(header, '')
    if header == "department":
        return dictionary.get(value, value)
    return value

def get_headers(dict_list: list):
    headers = []
    for dict in dict_list:
        for key in dict.keys():
            if not key in headers: 
                headers.append(key)
    return headers

def list_files_in_directory(directory):
    files = []
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path):
            files.append(full_path)
    return files

def get_file_extension(file_name):
    _, file_extension = os.path.splitext(file_name)
    return file_extension


if __name__ == '__main__':
    main()
