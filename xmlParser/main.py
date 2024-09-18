import os
import sys
from utils import get_lower_file_extension
from utils import clear_directory_from_csv_files
from guest import Guest
from csv_parser import CsvParser
from xml_parser import parse_xml


def get_current_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


out_dir = os.path.join(get_current_dir(), "out")
out_file = os.path.join(out_dir, "guests.csv")


description = f"""
Программа рекурсивно обходит xml по указанному пути, 
парсит их и составляет списки гостей в файлах без заголовков по {CsvParser.max_lines_per_file} строк. 
Результат в папке: {out_dir}"""


def main():
    print(description)
    while(True):
        guest_list = []
        in_dir = input("Путь к папке с xml:")
        if in_dir:
            clear_directory_from_csv_files(out_dir)
            for root, _, files in os.walk(in_dir):
                for file in files:
                    if get_lower_file_extension(file) == ".xml":
                        print(f"{file}")
                        file_path = os.path.join(root, file)
                        dictionary = parse_xml(file_path)
                        guest = Guest.dict_to_guest(dictionary)
                        if guest:
                            if not guest in guest_list:
                                guest_list.append(guest)
            csv_parser = CsvParser(out_file)
            csv_parser.write_guests_to_csv(guest_list, out_file)
        else:
            print(f"Путь не существует: {in_dir}")
        print(f"Работа завершена. Гостей в файлах: {len(guest_list)}")


if __name__ == "__main__":
    main()
