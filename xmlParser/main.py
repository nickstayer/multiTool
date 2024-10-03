import os
import sys
import utils
from guest import Guest
from csv_helper import CsvHelper
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
Заголовки csv (разделитель ',', кодировка 'utf-8'): Фамилия,Имя,Отчество,Год рождения,Код подразделения
Результат в папке: {out_dir}
"""

logger = Logger(log_dir)


def main():
    print(description)
    while(True):
        in_dir = utils.get_path(input("Путь к папке с файлами:"))
        if in_dir:
            logger.chapter()
            logger.log(f"Работа запущена. Источник файлов: {in_dir}")
            logger.log(f"Очищаю папку {out_dir}")
            
            utils.clear_directory_from_csv_files(out_dir)
            xml_files, csv_files = utils.get_xml_csv_files(in_dir)
            guest_list_xml = Guest.get_guests_from_xml_files(xml_files, logger)
            guest_list_csv = Guest.get_guests_from_csv_files(csv_files, logger)
            csv_helper = CsvHelper(out_file)
            csv_helper.write_guests_to_csv(guest_list_xml, out_file)
            csv_helper.write_guests_to_csv(guest_list_csv, out_file)
        else:
            logger.log(f"Путь не существует")
            continue

        guests_count = len(guest_list_xml) + len(guest_list_csv)
        logger.log(f"Гостей в файлах:\t{guests_count}")
        logger.log(f"Работа завершена.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.log(f"{e}")
