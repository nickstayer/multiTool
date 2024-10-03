import os
import re
from transliterator import Transliterator

def date_to_components(date: str):
    components = date.split('.')
    if len(components) < 3:
        return []
    new_components = []
    for c in components:
        if c.startswith('0'):
            new_components.append(c[1:])
        else:
            new_components.append(c)
    return new_components

def convert_date(date_str):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        year, month, day = date_str.split('-')
        return f"{day}.{month}.{year}"
    elif re.match(r'^\d{2}\.\d{2}\.\d{4}$', date_str):
        return date_str
    return None


def get_path(input: str):
    input = input.replace("\"", "")
    if os.path.exists(input):
        return input
    else:
        return None


def get_lower_file_extension(file_name):
    _, file_extension = os.path.splitext(file_name)
    return file_extension.lower()


def clear_directory_from_csv_files(directory_path):
    if os.path.exists(directory_path):
        try:
            if os.path.isdir(directory_path):
                print(f"Очищаю: {directory_path}")
                for filename in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, filename)
                    if os.path.isfile(file_path):
                        if get_lower_file_extension(file_path) == ".csv":
                            os.remove(file_path)
            else:
                print(f"Указанный путь '{directory_path}' не является директорией.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def get_xml_csv_files(path):
    xml_files, csv_files = [], []
    for root, _, files in os.walk(path):
        for file in files:
            ext = get_lower_file_extension(file)
            file_path = os.path.join(root, file)
            if ext == ".xml":
                xml_files.append(file_path)
            if ext == ".csv":
                csv_files.append(file_path)
    return xml_files, csv_files


def from_translit_to_ru(input):
    transliterator = Transliterator()
    prep_input = transliterator.preprocess_mixed_cyrillic_latin(input)
    return transliterator.to_cyrillic(prep_input)

