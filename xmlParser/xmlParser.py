import os
import sys
import xml.etree.ElementTree as ET
from guest import Guest


def get_current_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


out_dir = get_current_dir();
out_file = os.path.join(out_dir, "guests.csv")
max_lines_count = 1000

description = f"""
Программа рекурсивно обходит xml по указанному пути, 
парсит их и составляет списки гостей в файлах без заголовков по {max_lines_count} строк. 
Результат в папке: {out_dir}"""


def parse_element(element, parent_name=''):
    """Рекурсивно обрабатывает элементы XML и добавляет их в словарь."""
    parsed_data = {}
    tag_name = element.tag.split('}')[-1]
    full_tag_name = f"{parent_name}.{tag_name}" if parent_name else tag_name
    
    if element.text and element.text.strip():
        parsed_data[full_tag_name] = element.text.strip()
    
    if element.attrib:
        parsed_data[f"{full_tag_name}_attributes"] = element.attrib

    for child in element:
        parsed_data.update(parse_element(child, full_tag_name))

    return parsed_data


def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        parsed_data = parse_element(root)
        return parsed_data
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML: {e}")
        return None


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


def get_row(guest: Guest):
    date = date_to_components(guest.birthDate)
    if date:
        return f"{guest.lastName};{guest.firstName};{guest.middleName};{date[2]};{date[1]};{date[0]};{guest.supplierInfo}\n"
    return None


def get_new_file_name(counter: int, csv_file: str):
    if counter < max_lines_count:
        return csv_file
    elif counter % max_lines_count == 0:
        return csv_file.replace(".csv", f"_{int(counter / max_lines_count)}.csv")
    else:
        return csv_file


def write_to_csv(guest_list, csv_file):
    counter = 0
    current_file = csv_file
    for guest in guest_list:
        row = get_row(guest)
        if row:
            write(row, current_file)
            counter += 1
            new_file = get_new_file_name(counter, current_file)
            current_file = new_file
    return current_file


def write(row, csv_file):
    mode = "a"
    if(not os.path.exists(csv_file)):
        mode = "w"
    with open(csv_file, mode) as csvfile:
            csvfile.write(row)



def dict_to_guest(dictionary) -> Guest:
    if not 'case.declarant.person.lastName' in dictionary.keys():
        return None
    guest = Guest()
    for key, value in dictionary.items():
        if key == 'case.declarant.person.lastName':
            guest.lastName = value
        if key == 'case.declarant.person.firstName':
            guest.firstName = value
        if key == 'case.declarant.person.middleName':
            guest.middleName = value
        if key == 'case.declarant.person.birthDate':
            guest.birthDate = value
        if key == 'case.supplierInfo':
            guest.supplierInfo = value
    return guest


def get_path(input: str):
    input = input.replace("\"", "")
    if os.path.exists(input):
        return input
    else:
        return None


def get_lower_file_extension(file_name):
    _, file_extension = os.path.splitext(file_name)
    return file_extension.lower()


def clear_directory(directory_path):
    try:
        if os.path.isdir(directory_path):
            print(f"Очищаю: {directory_path}")
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            print(f"Указанный путь '{directory_path}' не является директорией.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def main():
    print(description)
    while(True):
        guest_list = []
        in_dir = input("Путь к папке с xml:")
        if in_dir:
            clear_directory(out_dir)
            for root, _, files in os.walk(in_dir):
                for file in files:
                    if get_lower_file_extension(file) == ".xml":
                        print(f"{file}")
                        file_path = os.path.join(root, file)
                        dictionary = parse_xml(file_path)
                        guest = dict_to_guest(dictionary)
                        if guest:
                            if not guest in guest_list:
                                guest_list.append(guest)
            write_to_csv(guest_list, out_file)
        else:
            print(f"Путь не существует: {in_dir}")
        print(f"Работа завершена. Гостей в файлах: {len(guest_list)}")


if __name__ == "__main__":
    main()