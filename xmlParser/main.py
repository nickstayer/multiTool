import os
import sys
from utils import get_xml_csv_files
from utils import clear_directory_from_csv_files
from guest import Guest
from csv_parser import CsvHelper
from xml_parser import parse_xml
from logger import Logger


def get_current_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

current_dir = get_current_dir()
out_dir = os.path.join(current_dir, "out")
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

out_file = os.path.join(out_dir, "guests_1.csv")

log_dir = os.path.join(current_dir, "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


description = f"""
Программа рекурсивно обходит xml, csv по указанному пути, 
парсит их и составляет списки гостей в файлах без заголовков по {CsvHelper.max_lines_per_file} строк.
Формат csv (разделитель не важен): Фамилия,Имя,Отчество,Год рождения,Код подразделения
Результат в папке: {out_dir}
"""

logger = Logger(log_dir)


def main():
    print(description)
    while(True):
        in_dir = input("Путь к папке с xml:")
        if in_dir:
            logger.chapter()
            logger.log(f"Работа запущена. Источник файлов: {in_dir}")
            logger.log(f"Очищаю папку {out_dir}")
            clear_directory_from_csv_files(out_dir)
            xml_files, csv_files = get_xml_csv_files(in_dir)
            guest_list_xml = get_guests_from_xml_files(xml_files)
            guest_list_csv = get_guests_from_csv_files(csv_files)
            csv_helper = CsvHelper(out_file)
            csv_helper.write_guests_to_csv(guest_list_xml, out_file)
            csv_helper.write_guests_to_csv(guest_list_csv, out_file)
        else:
            logger.log(f"Путь не существует: {in_dir}")

        guests_count = len(guest_list_xml) + len(guest_list_csv)
        logger.log(f"Гостей в файлах:\t{guests_count}")
        logger.log(f"Работа завершена.")


def get_guests_from_xml_files(files):
    guest_list = []
    file_counter = 0
    dub_counter = 0
    fail_counter = 0
    for file in files:
        file_counter += 1
        print(f"{file}")
        dictionary = parse_xml(file)
        guest = Guest.dict_to_guest(dictionary)
        if guest:
            guest.sourceFile = file
            if not guest in guest_list:
                guest_list.append(guest)
            else:
                in_list_guests = [g for g in guest_list if g == guest]
                logger.log(f"Внимание. Попытка добавить гостя:\t{guest}.\tФайл-источник:\t{guest.sourceFile}")
                for g in in_list_guests:
                    dub_counter += 1
                    logger.log(f"В списке уже есть гость с данными:\t{g}.\tФайл-источник:\t{g.sourceFile}")
        else:
            fail_counter += 1
            logger.log(f"Внимание. Не удалось получить информацию о госте:\t{file}")
    logger.paragraph()
    logger.log(f"Обработано xml:\t{file_counter}")
    logger.log(f"Попыток добавить дубли:\t{dub_counter}")
    logger.log(f"Не удалось получить информацию:\t{fail_counter}")
    return guest_list


def get_guests_from_csv_files(files):
    guest_list = []
    file_counter = 0
    fail_counter = 0
    for file in files:
        file_counter += 1
        print(f"{file}")
        dict_list = CsvHelper(file).read_csv()
        guests = Guest.dict_list_to_guests(dict_list)
        if guests:
            guest_list.extend(guests)
        else:
            fail_counter += 1
            logger.log(f"Внимание. Не удалось получить информацию о гостях:\t{file}")
    guest_set = set(guest_list)
    logger.paragraph()
    logger.log(f"Обработано csv:\t{file_counter}")
    logger.log(f"Попыток добавить дубли:\t{len(guest_list) - len(guest_set)}")
    logger.log(f"Не удалось получить информацию:\t{fail_counter}")
    return list(guest_set)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.log(f"{e}")
